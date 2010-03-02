# -*- coding: utf-8 -*-

"""
Kay auth application.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging

from google.appengine.ext import db
from werkzeug.utils import import_string

from kay.conf import settings
from kay.auth.models import DatastoreUser
from kay.utils.crypto import gen_pwhash
from kay.utils import local

class AuthError(Exception):
  pass

class DuplicateKeyError(AuthError):
  pass

def process_context(request):
  return {'user': request.user}

def login(request, **credentials):
  """
  If the given credentials are valid, return a User object.
  """
  backend = local.app.auth_backend
  try:
    user = backend.login(request, **credentials)
  except TypeError:
    # This backend doesn't accept these credentials as arguments.
    # Try the next one.
    pass
  return user or False

def logout(request):
  """
  Removes the authenticated user's ID from the request and flushes their
  session data.
  """
  from kay.sessions import flush_session
  flush_session(request)
  if hasattr(request, 'user'):
    from kay.auth.models import AnonymousUser
    request.user = AnonymousUser()

def create_new_user(user_name, password=None, **kwargs):
  try:
    auth_model = import_string(settings.AUTH_USER_MODEL)
  except (ImportError, AttributeError), e:
    logging.warn("Failed importing auth user model: %s." %
                 settings.AUTH_USER_MODEL)
    return
  if password:
    kwargs['password'] = auth_model.hash_password(password)
  else:
    kwargs['password'] = auth_model.get_unusable_password()
  def txn():
    user = auth_model.get_by_key_name(auth_model.get_key_name(user_name))
    if user:
      raise DuplicateKeyError("An user: %s is already registered." % user_name)
    new_user = auth_model(key_name=auth_model.get_key_name(user_name),
                          user_name=user_name, **kwargs)

    new_user.put()
    return new_user
  return db.run_in_transaction(txn)
