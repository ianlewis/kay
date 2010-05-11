# -*- coding: utf-8 -*-

"""
Kay authentication model for gaema.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp>,
                     Victor Goh <victorgoh@gmail.com>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import simplejson
import pickle

from google.appengine.ext import db


class GAEMAUser(db.Model):
  service = db.StringProperty(required=True)
  user_data = db.BlobProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True)
  updated = db.DateTimeProperty(auto_now=True)  

  @classmethod
  def get_or_insert(cls, key_name, user):
    ds_user = cls.get_by_key_name(key_name)
    if not ds_user or ds_user.raw_user_data != user:
      ds_user = cls.store_user_data(key_name, user)
    return ds_user

  @classmethod
  def store_user_data(cls, key_name, user):
    """You can override this class method for custom model."""
    ret = cls(key_name=key_name,
              user_data=pickle.dumps(user, pickle.HIGHEST_PROTOCOL),
              service=user['_service'])
    ret.put()
    return ret

  @property
  def raw_user_data(self):
    return pickle.loads(self.user_data)

  def is_anonymous(self):
    return False
        
  def is_authenticated(self):
    return True

  @property
  def is_admin(self):
    from google.appengine.api import users
    return users.is_current_user_admin()

  def __unicode__(self):
    """You may need to override this method according to how you store
    user data."""
    user_data = self.raw_user_data
    return user_data["name"]
