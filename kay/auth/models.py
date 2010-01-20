# -*- coding: utf-8 -*-

"""
Kay authentication models.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     Ian Lewis <IanMLewis@gmail.com>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from google.appengine.ext import db

from kay.conf import settings
from kay.utils import (
  crypto, render_to_string, url_for
)
from kay.i18n import lazy_gettext as _

class User(db.Model):
  """
  Basic user type that can be used with other login
  schemes other than Google logins
  """
  email = db.EmailProperty()
  first_name = db.StringProperty(required=False)
  last_name = db.StringProperty(required=False)
  is_admin = db.BooleanProperty(required=True, default=False)

  created = db.DateTimeProperty(auto_now_add=True)
  updated = db.DateTimeProperty(auto_now=True)

  def __unicode__(self):
    return unicode(self.email)

  def __str__(self):
    return self.__unicode__()

  def is_anonymous(self):
    return False

  def is_authenticated(self):
    return True

  def __eq__(self, obj):
    if not obj:
      return False
    return self.key() == obj.key()

  def __ne__(self, obj):
    return not self.__eq__(obj)

class DatastoreUserDBOperationMixin(object):

  @classmethod
  def create_inactive_user(cls, user_name, password, email, send_email=True):
    import datetime
    from kay.registration.models import RegistrationProfile
    from google.appengine.api.labs import taskqueue
    def txn():
      key_name = cls.get_key_name(user_name)
      user = cls.get_by_key_name(key_name)
      if user:
        from kay.auth import DuplicateKeyError
        raise DuplicateKeyError(_(u"This user name is already taken."
                                  " Please choose another user name."))
      salt = crypto.gen_salt()
      activation_key = crypto.sha1(salt+user_name).hexdigest()
      profile_key = db.Key.from_path(cls.kind(), key_name,
                                     RegistrationProfile.kind(),
                                     activation_key)

      expiration_date = datetime.datetime.now() + \
          datetime.timedelta(seconds=settings.ACCOUNT_ACTIVATION_DURATION)
      taskqueue.add(url=url_for('_internal/expire_registration',
                                registration_key=str(profile_key)),
                    eta=expiration_date, transactional=True)
      taskqueue.add(url=url_for('_internal/send_registration_confirm',
                                registration_key=str(profile_key)),
                    transactional=True)
      user = cls(key_name=key_name, activated=False, user_name=user_name,
                 password=crypto.gen_pwhash(password), email=email)
      profile = RegistrationProfile(user=user, parent=user,
                                    key_name=activation_key)
      db.put([profile, user])
      return user
    user = db.run_in_transaction(txn)
    return user

  @classmethod
  def get_key_name(cls, user_name):
    return 'u:%s' % user_name

  @classmethod
  def get_by_user_name(cls, user_name):
    return cls.get_by_key_name(cls.get_key_name(user_name))

  @classmethod
  def hash_password(cls, raw):
    return crypto.gen_pwhash(raw)

  @classmethod
  def get_unusable_password(cls):
    return 'unusable_password'

  def check_password(self, raw_password):
    if hasattr(self, 'activated') and self.activated is False:
      return False
    return crypto.check_pwhash(self.password, raw_password)

  def set_password(self, raw_password):
    self.password = self.hash_password(raw_password)
    return self.put()

class DatastoreUser(User, DatastoreUserDBOperationMixin):
  """
  Use DatastoreUser.get_key_name(user_name) as key_name for this model.
  """
  activated = db.BooleanProperty(required=True, default=True)
  user_name = db.StringProperty(required=True)
  password = db.StringProperty(required=True)

  def __unicode__(self):
    return unicode(self.user_name)


class GoogleUser(User):
  """
  Use User.user_id() as key_name for this model.
  """
  def __eq__(self, obj):
    if not obj or obj.is_anonymous():
      return False
    import os
    if 'SERVER_SOFTWARE' in os.environ and \
          os.environ['SERVER_SOFTWARE'].startswith('Dev'):
      # It allows us to pose as an user in dev server.
      return self.email == obj.email
    else:
      return self.key() == obj.key()

class HybridUser(GoogleUser, DatastoreUserDBOperationMixin):
  """GoogleUser/DatastoreUser hybrid model.
  """
  activated = db.BooleanProperty(required=True, default=True)
  user_name = db.StringProperty(required=False)
  password = db.StringProperty(required=False)

  def __unicode__(self):
    if self.user_name:
      return unicode(self.user_name)
    return unicode(self.email)

class AnonymousUser(object):
  __slots__ = ('is_admin')
  is_admin = False

  def __unicode__(self):
    return u"AnonymousUser"

  def __str__(self):
    return self.__unicode__()

  def is_anonymous(self):
    return True

  def is_authenticated(self):
    return False

  def key(self):
    return None

  def __eq__(self, obj):
    return False

  def __ne__(self, obj):
    return not self.__eq__(obj)


class TemporarySession(db.Model):
  """
  Set an unique id as key_name.
  """
  user = db.ReferenceProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True)
  last_login = db.DateTimeProperty(auto_now=True)
  data = db.BlobProperty()

  @classmethod
  def get_key_name(cls, uuid):
    return 's:%s' % uuid

  @classmethod
  def get_new_session(cls, user, data=None, auto_delete=True,
                      countdown=settings.TEMPORARY_SESSION_LIFETIME,
                      additional_tq_url=None, tq_kwargs={}):
    from kay.utils import crypto
    from google.appengine.api.labs import taskqueue
    def txn(id):
      key_name = cls.get_key_name(id)
      if additional_tq_url is not None:
        tq_kwargs.update({'session_key': db.Key.from_path(cls.kind(),
                                                          key_name)})
        taskqueue.add(url=url_for(additional_tq_url, **tq_kwargs),
                      transactional=True)
      taskqueue.add(url=url_for("_internal/expire_temporary_session",
                                session_key=db.Key.from_path(cls.kind(),
                                                             key_name)),
                    countdown=countdown, transactional=True)
      session = cls.get_by_key_name(key_name)
      if session is None:
        if data:
          session = cls(key_name=key_name, user=user, data=data)
        else:
          session = cls(key_name=key_name, user=user)
        session.put()
        return session
      else:
        raise db.Rollback("The specified id already exists.")

    id = crypto.new_iid()
    session = db.run_in_transaction(txn, id)
    while session is None:
      id = crypto.new_iid()
      session = db.run_in_transaction(txn, id)
    return session
