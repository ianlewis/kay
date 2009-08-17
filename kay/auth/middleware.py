# -*- coding: utf-8 -*-

"""
Middleware for authentication.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from kay import auth
from kay.exceptions import ImproperlyConfigured
from kay.conf import settings
from kay.utils.importlib import import_module
from kay.utils import local

class LazyUser(object):
  def __get__(self, request, obj_type=None):
    if not hasattr(request, '_cached_user'):
      request._cached_user = local.app.auth_backend.get_user(request)
    return request._cached_user


class AuthenticationMiddleware(object):
  def process_request(self, request):
    if not hasattr(request, 'session'):
      raise ImproperlyConfigured(
        "The Django authentication middleware requires session middleware to "
        "be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
        "'kay.sessions.middleware.SessionMiddleware'.")
    request.__class__.user = LazyUser()
    return None


class LazyGoogleUser(object):
  """
  A lazily evaluated object that contains information
  about the current user.
  WARNING: Should not be used for anything but the CURRENT user.
  """  
  def __get__(self, request, obj_type=None):
    if not hasattr(request, '_cached_user'):
      from kay.auth.models import AnonymousUser
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
      from google.appengine.api import users
      from google.appengine.ext import db
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
        request._cached_user = db.run_in_transaction(txn)
      else:
        request._cached_user = AnonymousUser()
    return request._cached_user


class GoogleAuthenticationMiddleware(object):
  def process_request(self, request):
    request.__class__.user = LazyGoogleUser()
    return None
