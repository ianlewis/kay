# -*- coding: utf-8 -*-

from kay import auth
from kay.exceptions import ImproperlyConfigured


class LazyUser(object):
  def __get__(self, request, obj_type=None):
    if not hasattr(request, '_cached_user'):
      from kay.auth import get_user
      request._cached_user = get_user(request)
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
  def __get__(self, request, obj_type=None):
    if not hasattr(request, '_cached_user'):
      from kay.auth.models import AnonymousUser, GoogleUser
      from google.appengine.api import users
      from google.appengine.ext import db
      user = users.get_current_user()
      if user:
        key_name = '_%s' % user.user_id()
        email = user.email()
        def txn():
          entity = GoogleUser.get_by_key_name(key_name)
          if entity is None:
            entity = GoogleUser(key_name=key_name, email=email)
            entity.put()
          elif entity.email != email:
            entity.email = email
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
