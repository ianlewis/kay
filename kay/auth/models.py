# -*- coding: utf-8 -*-

"""
Kay authentication models.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import pytz
from google.appengine.ext import db

from kay.conf import settings

class GoogleUser(db.Model):
  """
  Use User.user_id() as key_name for this model.
  """
  email = db.EmailProperty(required=True)
  first_name = db.StringProperty(required=False)
  last_name = db.StringProperty(required=False)
  tz = db.StringProperty(choices=pytz.all_timezones, required=True,
                         default=settings.DEFAULT_TIMEZONE,
                         indexed=False)
  created = db.DateTimeProperty(auto_now_add=True)
  last_login = db.DateTimeProperty(auto_now=True)

  def __unicode__(self):
    return unicode(self.email)

  def is_anonymous(self):
    return False

  def is_authenticated(self):
    return True

class AnonymousUser(object):
  __slots__ = ('tz')
  tz = settings.DEFAULT_TIMEZONE

  def __unicode__(self):
    return "AnonymousUser"

  def is_anonymous(self):
    return True

  def is_authenticated(self):
    return False
