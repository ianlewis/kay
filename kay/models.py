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
  def get_key_generator(cls, **kwargs):
    while 1:
      yield crypto.new_iid()

  @classmethod
  def create_new_entity(cls, **kwargs):
    def txn(key_name):
      if kwargs.has_key('parent'):
        entity = cls.get_by_key_name(key_name, parent=kwargs['parent'])
      else:
        entity = cls.get_by_key_name(key_name)
      if entity is None:
        entity = cls(key_name=key_name, **kwargs)
        entity.put()
        return entity
      else:
        return None
    key_generator = cls.get_key_generator(**kwargs)
    first_key_name = key_generator.next()
    entity = db.run_in_transaction(txn, first_key_name)
    while entity is None:
      key_name = key_negerator.next()
      entity = db.run_in_transaction(txn, key_name)
    return entity
