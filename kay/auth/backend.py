# -*- coding: utf-8 -*-

"""
Kay authentication backends.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from google.appengine.ext import db
from werkzeug.urls import url_quote_plus

from kay.exceptions import ImproperlyConfigured
from kay.conf import settings
from kay.utils import (
  local, url_for
)
from kay.auth.models import AnonymousUser
from kay.utils.importlib import import_module
from kay.misc import get_appid

class DatastoreBackend(object):
  
  def get_user(self, request):
    if request.session.has_key('_user'):
      return db.get(request.session['_user'])
    else:
      return AnonymousUser()

  def create_login_url(self, url):
    return url_for("auth/login", next=url_quote_plus(url))

  def create_logout_url(self, url):
    return url_for("auth/logout", next=url_quote_plus(url))

  def logout(self):
    try:
      del local.request.session['_user']
    except:
      pass

  def store_user(self, user):
    from kay.sessions import renew_session
    renew_session(local.request)
    local.request.session['_user'] = user.key()
    return True

  def login(self, user_name, password):
    try:
      dot = settings.AUTH_USER_MODEL.rindex(".")
    except ValueError:
      raise ImproperlyConfigured, \
          '%s isn\'t a auth user model.' % settings.AUTH_USER_MODEL
    auth_model_module = settings.AUTH_USER_MODEL[:dot]
    auth_model_classname = settings.AUTH_USER_MODEL[dot+1:]
    try:
      mod = import_module(auth_model_module)
    except ImportError, e:
      raise ImproperlyConfigured, \
          'Error importing auth model %s: "%s"' % (auth_model_module, e)
    try:
      auth_model_class = getattr(mod, auth_model_classname)
    except AttributeError:
      raise ImproperlyConfigured, \
          'Auth model module "%s" does not define a "%s" class' % \
          (auth_model_module, auth_model_classname)
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
