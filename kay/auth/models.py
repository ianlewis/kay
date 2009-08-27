# -*- coding: utf-8 -*-

"""
Kay authentication models.

:copyright: (c) 2009 by Accense Technology, Inc. See AUTHORS for more
details.
:license: BSD, see LICENSE for more details.
"""

from google.appengine.ext import db

from kay.conf import settings
from kay.utils import crypto

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
  last_login = db.DateTimeProperty(auto_now=True)

  def __unicode__(self):
    return unicode(self.email)

  def is_anonymous(self):
    return False

  def is_authenticated(self):
    return True

class DatastoreUser(User):
  """
  Use DatastoreUser.get_key_name(user_name) as key_name for this model.
  """
  user_name = db.StringProperty(required=True)
  password = db.StringProperty(required=True)

  def __unicode__(self):
    return unicode(self.user_name)

  @classmethod
  def get_key_name(cls, user_name):
    return 'u:%s' % user_name

  @classmethod
  def get_by_user_name(cls, user_name):
    return cls.get_by_key_name(cls.get_key_name(user_name))

  def check_password(self, raw_password):
    return crypto.check_pwhash(self.password, raw_password)

  def set_password(self, raw_password):
    self.password = crypto.gen_pwhash(raw_password)
    return self.put()

class GoogleUser(User):
  """
  Use User.user_id() as key_name for this model.
  """
  pass


class AnonymousUser(object):
  __slots__ = ('is_admin')
  is_admin = False

  def __unicode__(self):
    return "AnonymousUser"

  def is_anonymous(self):
    return True

  def is_authenticated(self):
    return False

  def key(self):
    return None

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
    def txn():
      uuid = crypto.new_iid()
      session = cls.get_by_key_name(cls.get_key_name(uuid))
      while session is not None:
        uuid = crypto.new_iid()
        session = cls.get_by_key_name(cls.get_key_name(uuid))
      session = cls(key_name=cls.get_key_name(uuid), user=user)
      session.put()
      return session
    return db.run_in_transaction(txn)
