# -*- coding: utf-8 -*-

"""
Kay utils.db_hook module.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from google.appengine.api import datastore
from google.appengine.ext import db

post_save_hooks = {}

NEWLY_CREATED = 1
UPDATED = 2
MAYBE_NEWLY_CREATED = 3
MAYBE_UPDATED = 4
UNKOWN = 5

def register_post_save_hook(func, model):
  global post_save_hooks
  kind = model.kind()
  func_list = post_save_hooks.get(kind, None)
  if func_list is None:
    func_list = []
  func_list.append(func)
  post_save_hooks[kind] = func_list

def execute_hooks(kind, key, entity):
  put_type = UNKOWN
  func_list = post_save_hooks.get(kind, None)
  if func_list is not None:
    last_path = entity.key().path().element_list()[-1]
    has_name = last_path.has_name()
    if last_path.has_id():
      if last_path.id() == 0:
        put_type = NEWLY_CREATED
      else:
        put_type = UPDATED
    entity.key_.CopyFrom(key)
    e = datastore.Entity._FromPb(entity)
    instance = db.class_for_kind(kind).from_entity(e)
    if has_name:
      if hasattr(instance, "created"):
        import datetime
        threshold = datetime.timedelta(0,0,1000)
        if hasattr(instance, "updated"):
          if abs(instance.created - instance.updated) < threshold:
            put_type = MAYBE_NEWLY_CREATED
          else:
            put_type = MAYBE_UPDATED
        else:
          if (datetime.datetime.now() - instance.created) < threshold:
            put_type = MAYBE_NEWLY_CREATED
          else:
            put_type = MAYBE_UPDATED
    for func in func_list:
      func(instance, put_type)
