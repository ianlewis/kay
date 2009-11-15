# -*- coding: utf-8 -*-

"""
Kay registration models.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import datetime

from google.appengine.ext import db

from kay.conf import settings

class RegistrationProfile(db.Model):
  user = db.ReferenceProperty()
  activated = db.BooleanProperty(required=True, default=False)

  @classmethod
  def activate_user(cls, activation_key):
    target = db.get(activation_key)
    if target is None or target.activation_key_expired:
      return None
    def txn():
      target.user.activated = True
      target.user.put()
      target.activated = True
      target.put()
      return target
    target = db.run_in_transaction(txn)
    return target.user

  @property
  def activation_key_expired(self):
    expiration_date = datetime.timedelta(
      seconds=settings.ACCOUNT_ACTIVATION_DURATION)
    return self.activated or \
        (self.user.created + expiration_date <= datetime.datetime.now())

def expire_registration(registration_key):
  p = RegistrationProfile.get(registration_key)
  def txn():
    if not p.activated:
      p.user.delete()
    p.delete()
  db.run_in_transaction(txn)
