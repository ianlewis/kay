# -*- coding: utf-8 -*-

"""
Kay authentication backends.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from google.appengine.ext import db
from google.appengine.api import users
from werkzeug.urls import url_quote_plus
from werkzeug.utils import import_string

from kay.exceptions import ImproperlyConfigured
from kay.conf import settings
from kay.utils import (
  local, url_for
)
from kay.auth.models import AnonymousUser
from kay.misc import get_appid

class GoogleBackend(object):
  def get_user(self, request):
    from kay.auth.models import AnonymousUser
    try:
      auth_model_class = import_string(settings.AUTH_USER_MODEL)
    except (ImportError, AttributeError), e:
      raise ImproperlyConfigured, \
          'Failed to import %s: "%s".' % (settings.AUTH_USER_MODEL, e)
    user = users.get_current_user()
    if user:
      key_name = '_%s' % user.user_id()
      email = user.email()
      is_current_user_admin = users.is_current_user_admin()
      def txn():
        entity = auth_model_class.get_by_key_name(key_name)
        if entity is None:
          entity = auth_model_class(
            key_name=key_name,
            email=email,
            is_admin=is_current_user_admin,
          )
          entity.put()
        else:
          update_user = False
          if entity.is_admin != is_current_user_admin:
            entity.is_admin = is_current_user_admin
            update_user = True
          if entity.email != email:
            entity.email = email
            update_user = True
          if update_user:
            entity.put()
        return entity
      return db.run_in_transaction(txn)
    else:
      return AnonymousUser()

  def create_login_url(self, url):
    return users.create_login_url(url)

  def create_logout_url(self, url):
    return users.create_logout_url(url)

  def login(self, request, user_name, password):
    return
      

class DatastoreBackend(object):
  def __init__(self):
    if not 'kay.sessions.middleware.SessionMiddleware' in \
          settings.MIDDLEWARE_CLASSES:
      raise ImproperlyConfigured(
        "The Kay authentication middleware requires session middleware to "
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
    from models import TemporarySession
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
