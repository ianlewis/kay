# -*- coding: utf-8 -*-

"""
Kay utils.db_hook module.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from google.appengine.api import datastore
from google.appengine.ext import db

post_save_hooks = {}


def register_post_save_hook(func, model):
  global post_save_hooks
  kind = model.kind()
  func_list = post_save_hooks.get(kind, None)
  if func_list is None:
    func_list = []
  func_list.append(func)
  post_save_hooks[kind] = func_list

def execute_hooks(kind, key, entity):
  func_list = post_save_hooks.get(kind, None)
  if func_list is not None:
    entity.key_.CopyFrom(key)
    e = datastore.Entity._FromPb(entity)
    instance = db.class_for_kind(kind).from_entity(e)
    for func in func_list:
      func(instance)
