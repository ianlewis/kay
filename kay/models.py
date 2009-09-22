# -*- coding: utf-8 -*-

"""
kay.models

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""


from google.appengine.ext import db
from kay.utils import crypto

class NamedModel(db.Model):
  """ This base model has a classmethod for automatically asigning a
  new uuid for its key_name on creation of a new entity.
  """
  @classmethod
  def create_new_entity(cls, **kwargs):
    def txn():
      uuid = crypto.new_iid()
      if kwargs.has_key('parent'):
        entity = cls.get_by_key_name(uuid, parent=kwargs['parent'])
      else:
        entity = cls.get_by_key_name(uuid)
      while entity is not None:
        uuid = crypto.new_iid()
        if kwargs.has_key('parent'):
          entity = cls.get_by_key_name(uuid, parent=kwargs['parent'])
        else:
          entity = cls.get_by_key_name(uuid)
      entity = cls(key_name=uuid, **kwargs)
      entity.put()
      return entity
    return db.run_in_transaction(txn)

