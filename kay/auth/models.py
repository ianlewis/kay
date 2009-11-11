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
  crypto, render_to_string
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
    from kay.registration.models import RegistrationProfile
    def txn():
      key_name = cls.get_key_name(user_name)
      user = cls.get_by_key_name(key_name)
      if user:
        from kay.auth import DuplicateKeyError
        raise DuplicateKeyError(_(u"This user name is already taken."
                                  " Please choose another user name."))
      user = cls(key_name=key_name, activated=False, user_name=user_name,
                 password=crypto.gen_pwhash(password), email=email)
      user.put()
      return user
    user = db.run_in_transaction(txn)
    salt = crypto.gen_salt()
    activation_key = crypto.sha1(salt+user.user_name).hexdigest()
    profile = RegistrationProfile(user=user, key_name=activation_key)
    profile.put()
    from google.appengine.api import mail
    subject = render_to_string('registration/activation_email_subject.txt',
                               {'appname': settings.APP_NAME})
    subject = ''.join(subject.splitlines())
    message = render_to_string(
      'registration/activation_email.txt',
      {'activation_key': activation_key,
       'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
       'appname': settings.APP_NAME})
    mail.send_mail(subject=subject, body=message,
                   sender=settings.DEFAULT_MAIL_FROM, to=user.email)
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

  @classmethod
  def get_key_name(cls, uuid):
    return 's:%s' % uuid

  @classmethod
  def get_new_session(cls, user):
    from kay.utils import crypto
    def txn(id):
      session = cls.get_by_key_name(cls.get_key_name(id))
      if session is None:
        session = cls(key_name=cls.get_key_name(id), user=user)
        session.put()
        return session
      else:
        return None

    id = crypto.new_iid()
    session = db.run_in_transaction(txn, id)
    while session is None:
      id = crypto.new_iid()
      session = db.run_in_transaction(txn, id)
    return session
