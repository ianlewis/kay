# -*- coding: utf-8 -*-

"""
Middleware for authentication.

:Copyright: (c) 2009 Accense Technology, Inc.,
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     Ian Lewis <IanMLewis@gmail.com>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from werkzeug.utils import import_string

from kay import auth
from kay.exceptions import ImproperlyConfigured
from kay.conf import settings
from kay.utils import local

class LazyUser(object):
  def __get__(self, request, obj_type=None):
    if not hasattr(request, '_cached_user'):
      request._cached_user = local.app.auth_backend.get_user(request)
    return request._cached_user


class AuthenticationMiddleware(object):
  def process_request(self, request):
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
        auth_model_class = import_string(settings.AUTH_USER_MODEL)
      except (ImportError, AttributeError), e:
        raise ImproperlyConfigured, \
            'Failed to import %s: "%s".' % (settings.AUTH_USER_MODEL, e)
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
