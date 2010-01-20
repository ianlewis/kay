# -*- coding: utf-8 -*-

"""
Kay authentication backend with user information stored in the
datastore.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from google.appengine.ext import db
from werkzeug.urls import url_quote_plus
from werkzeug.utils import import_string

from kay.exceptions import ImproperlyConfigured
from kay.conf import settings
from kay.utils import (
  local, url_for
)
from kay.auth.models import AnonymousUser
from kay.misc import get_appid


class DatastoreBackend(object):
  def __init__(self):
    if not 'kay.sessions.middleware.SessionMiddleware' in \
          settings.MIDDLEWARE_CLASSES:
      raise ImproperlyConfigured(
        "The DatastoreBackend requires session middleware to "
        "be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
        "'kay.sessions.middleware.SessionMiddleware'.")
  
  def get_user(self, request):
    if request.session.has_key('_user'):
      return db.get(request.session['_user'])
    else:
      return AnonymousUser()

  def create_login_url(self, url):
    return url_for("auth/login", next=url_quote_plus(url))

  def create_logout_url(self, url):
    return url_for("auth/logout", next=url_quote_plus(url))

  def store_user(self, user):
    from kay.sessions import renew_session
    renew_session(local.request)
    local.request.session['_user'] = user.key()
    return True

  def login(self, request, user_name, password):
    try:
      auth_model_class = import_string(settings.AUTH_USER_MODEL)
    except (ImportError, AttributeError), e:
      raise ImproperlyConfigured, \
          'Failed to import %s: "%s".' % (settings.AUTH_USER_MODEL, e)
    user = auth_model_class.get_by_user_name(user_name)
    if user is None:
      return False
    if user.check_password(password):
      return self.store_user(user)
    return False

class DatastoreBackendWithOwnedDomainHack(DatastoreBackend):

  def store_user(self, user):
    from kay.auth.models import TemporarySession
    session = TemporarySession.get_new_session(user)
    return session

  def create_login_url(self, url):
    import os
    hostname = get_appid() + '.appspot.com'
    url = url_for("auth/login",
                  next=url_quote_plus(url),
                  original_host_url=url_quote_plus(local.request.host_url),
                  owned_domain_hack=True)
    if 'SERVER_SOFTWARE' in os.environ and \
          os.environ['SERVER_SOFTWARE'].startswith('Dev'):
      return url
    else:
      return "https://%s%s" % (hostname, url)
