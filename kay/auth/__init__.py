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

class AuthError(Exception):
  pass

class DuplicateKeyError(AuthError):
  pass

def process_context(request):
  return {'user': request.user}


def create_new_user(user_name, password, is_admin=False):
  try:
    auth_model = import_string(settings.AUTH_USER_MODEL)
  except (ImportError, AttributeError), e:
    logging.warn("Failed importing auth user model: %s." %
                 settings.AUTH_USER_MODEL)
    return
  def txn():
    user = auth_model.get_by_key_name(auth_model.get_key_name(user_name))
    if user:
      raise DuplicateKeyError("An user: %s is already registered." % user_name)
    new_user = auth_model(key_name=auth_model.get_key_name(user_name),
                          user_name=user_name, password=gen_pwhash(password),
                          is_admin=is_admin)
    new_user.put()
    return new_user
  return db.run_in_transaction(txn)
