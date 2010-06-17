# -*- coding: utf-8 -*-

"""
Kay authentication backend using google account.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from google.appengine.ext import db
from google.appengine.api import users
from werkzeug.utils import import_string

from kay.exceptions import ImproperlyConfigured
from kay.conf import settings
from kay.auth.models import AnonymousUser

class GoogleBackend(object):
  def get_user(self, request):
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

  def create_login_url(self, url, **kwargs):
    return users.create_login_url(url, **kwargs)

  def create_logout_url(self, url, **kwargs):
    return users.create_logout_url(url, **kwargs)

  def login(self, request, user_name, password):
    return

  def test_login(self, client, email='', is_admin=''):
    import os
    os.environ['USER_EMAIL'] = email
    os.environ['USER_IS_ADMIN'] = '1' if is_admin else ''

  def test_logout(self, client):
    import os
    os.environ['USER_EMAIL'] = ''
    os.environ['USER_IS_ADMIN'] = ''
