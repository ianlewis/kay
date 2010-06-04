# -*- coding: utf-8 -*-

"""
Kay authentication backend using gaema.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp>,
                     Victor Goh <victorgoh@gmail.com>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging
from urllib import quote_plus

from werkzeug import redirect
from werkzeug.utils import import_string
from werkzeug.urls import url_quote_plus

from kay.utils import (
  render_to_response, reverse,
  get_by_key_name_or_404, get_by_id_or_404,
  to_utc, to_local_timezone, url_for, raise_on_dev, local
)
from kay.auth.models import AnonymousUser
from kay.ext.gaema.utils import (
  get_gaema_user, get_valid_services, create_gaema_logout_url,
  create_marketplace_login_url, create_marketplace_logout_url,
  set_gaema_user,
)
from kay.ext.gaema import (
  services, GAEMA_USER_KEY_FORMAT
)
from kay.ext.gaema.models import GAEMAUser
from kay.conf import settings
from kay.exceptions import ImproperlyConfigured
from kay.auth.models import AnonymousUser

class GAEMABackend(object):

  def __init__(self):
    self.user_model = getattr(settings, 'GAEMA_USER_MODEL', GAEMAUser)
    if isinstance(self.user_model, basestring):
      try:
        self.user_model = import_string(self.user_model)
      except Exception:
        raise ImproperlyConfigured("Failed to import %s" % self.user_model)
    self.valid_services = get_valid_services()

  def get_user(self, request):
    '''check for gaema authenticated user and return the user
    '''
    if hasattr(request, settings.MARKETPLACE_DOMAIN_NAME_KEY):
      # marketplace
      domain = getattr(request, settings.MARKETPLACE_DOMAIN_NAME_KEY)
      user = get_gaema_user(domain)
      if user:
        user['_service'] = domain
        key_name = "%s:%s" % (domain, user['claimed_id'])
        return self.user_model.get_or_insert(key_name, user)
      else:
        return AnonymousUser()
    for service in self.valid_services:
      user = get_gaema_user(service)
      if user:
        user['_service'] = service
        key_name = services.get_key_name(user)
        return self.user_model.get_or_insert(key_name, user)
    return AnonymousUser()

  def create_login_url(self, next_url='/'):
    if hasattr(local.request, settings.MARKETPLACE_DOMAIN_NAME_KEY):
      # marketplace
      domain = getattr(local.request, settings.MARKETPLACE_DOMAIN_NAME_KEY)
      return create_marketplace_login_url(domain, next_url)
    return url_for('gaema/select_service',
                   targets='|'.join(self.valid_services),
                   next_url=url_quote_plus(next_url))

  def create_logout_url(self, next_url='/'):
    if hasattr(local.request, settings.MARKETPLACE_DOMAIN_NAME_KEY):
      # marketplace
      domain = getattr(local.request, settings.MARKETPLACE_DOMAIN_NAME_KEY)
      return create_marketplace_logout_url(domain, next_url)
    user = self.get_user(local.request)
    return create_gaema_logout_url(user.service, nexturl=next_url)

  def login(self, request, user_name, password):
    pass

  def test_login_or_logout(self, client, service, user_data):
    from cookielib import Cookie
    args = [None, None, '', None, None, '/', None, None, 86400, None, None,
            None, None]
    gaema_user_key = GAEMA_USER_KEY_FORMAT % service
    if hasattr(settings, "GAEMA_STORAGE") and \
          settings.GAEMA_STORAGE == "cookie":
      client.cookie_jar.set_cookie(Cookie(1, gaema_user_key, user_data, *args))
    else:
      session_store = import_string(settings.SESSION_STORE)()
      data = None
      for cookie in client.cookie_jar:
        if cookie.name == settings.COOKIE_NAME:
          data = cookie.value
      if data is None:
        session = session_store.new()
      else:
        session = session_store.get(data)
      session[gaema_user_key] = user_data
      session_store.save(session)
      data = "\"%s\"" % session_store.get_data(session)
      client.cookie_jar.set_cookie(Cookie(1, settings.COOKIE_NAME,
                                          data,
                                          *args))

  def test_login(self, client, service, user_data):
    self.test_login_or_logout(client, service, user_data)

  def test_logout(self, client, service):
    self.test_login_or_logout(client, service, '')
    
