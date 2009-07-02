# -*- coding: utf-8 -*-

"""
Kay authentication models.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from google.appengine.ext import db

from kay.conf import settings

class User(db.Model):
  """
  Basic user type that can be used with other login
  schemes other than Google logins
  """
  email = db.EmailProperty(required=True)
  first_name = db.StringProperty(required=False)
  last_name = db.StringProperty(required=False)

  created = db.DateTimeProperty(auto_now_add=True)
  last_login = db.DateTimeProperty(auto_now=True)

  def __unicode__(self):
    return unicode(self.email)

  def is_anonymous(self):
    return False

  def is_authenticated(self):
    return True

class GoogleUser(User):
  """
  Use User.user_id() as key_name for this model.
  """
  is_admin = db.BooleanProperty(required=True, default=False)

class AnonymousUser(object):
  __slots__ = ('tz')
  tz = settings.DEFAULT_TIMEZONE

  def __unicode__(self):
    return "AnonymousUser"

  def is_anonymous(self):
    return True

  def is_authenticated(self):
    return False

  def key(self):
    return None
