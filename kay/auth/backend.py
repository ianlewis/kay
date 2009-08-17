# -*- coding: utf-8 -*-

"""
Kay authentication backends.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import urllib2

from kay.exceptions import ImproperlyConfigured
from kay.conf import settings
from kay.utils import (
  local, url_for
)
from kay.auth.models import AnonymousUser
from kay.utils.importlib import import_module

class DatastoreBackend(object):
  
  def get_user(self, request):
    if request.session.has_key('_user'):
      return request.session['_user']
    else:
      return AnonymousUser()

  def create_login_url(self, url):
    return url_for("auth/login", next=urllib2.quote(url,safe=''))

  def create_logout_url(self, url):
    return url_for("auth/logout", next=urllib2.quote(url,safe=''))

  def logout(self):
    try:
      del local.request.session['_user']
    except:
      pass

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
      local.request.session['_user'] = user
      return True
    return False
