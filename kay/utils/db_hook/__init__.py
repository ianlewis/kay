# -*- coding: utf-8 -*-

"""
Kay utils.db_hook module.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from google.appengine.api import datastore
from google.appengine.ext import db

from kay.utils import local

import put_type

post_save_hooks = {}

def register_post_save_hook(func, model):
  global post_save_hooks
  kind = model.kind()
  func_list = post_save_hooks.get(kind, None)
  if func_list is None:
    func_list = []
  func_list.append(func)
  post_save_hooks[kind] = func_list

def get_created_datetime(entity):
  for key, prop in entity.fields().iteritems():
    if hasattr(prop, 'auto_now_add') and prop.auto_now_add:
      return getattr(entity, key)

def get_updated_datetime(entity):
  for key, prop in entity.fields().iteritems():
    if hasattr(prop, 'auto_now') and prop.auto_now:
      return getattr(entity, key)  

def execute_hooks(kind, key, entity):
  put_type_id = put_type.UNKOWN
  func_list = post_save_hooks.get(kind, None)
  if func_list is not None:
    last_path = entity.key().path().element_list()[-1]
    has_name = last_path.has_name()
    if last_path.has_id():
      if last_path.id() == 0:
        put_type_id = put_type.NEWLY_CREATED
      else:
        put_type_id = put_type.UPDATED
    entity.key_.CopyFrom(key)
    e = datastore.Entity._FromPb(entity)
    instance = db.class_for_kind(kind).from_entity(e)
    if has_name:
      created = get_created_datetime(instance)
      updated = get_updated_datetime(instance)
      if created:
        import datetime
        threshold = datetime.timedelta(0,0,1000)
        if updated:
          if abs(created - updated) < threshold:
            put_type_id = put_type.MAYBE_NEWLY_CREATED
          else:
            put_type_id = put_type.MAYBE_UPDATED
        else:
          if (datetime.datetime.now() - created) < threshold:
            put_type_id = put_type.MAYBE_NEWLY_CREATED
          else:
            put_type_id = put_type.MAYBE_UPDATED
    if datastore._CurrentTransactionKey():
      # This operation is inside the transaction. So, we reserve the
      # func_list and parameters for later execution.
      tmp_list = getattr(local, '_reserved_hooks', None)
      if tmp_list is None:
        tmp_list = []
      tmp_list.append((func_list, instance, put_type_id))
      local._reserved_hooks = tmp_list
    else:
      for func in func_list:
        func(instance, put_type_id)

def clear_reserved_hooks():
  tmp_list = getattr(local, '_reserved_hooks', None)
  if tmp_list is not None:
    local._reserved_hooks = []

def execute_reserved_hooks():
  tmp_list = getattr(local, '_reserved_hooks', None)
  if tmp_list is not None:
    for func_list, instance, put_type_id in tmp_list:
      for func in func_list:
        func(instance, put_type_id)

def model_name_from_key(key):
  return key.path().element_list()[0].type()

def post_hook(service, call, request, response):
  if call == 'Put':
    for key, entity in zip(response.key_list(), request.entity_list()):
      kind = model_name_from_key(key)
      execute_hooks(kind, key, entity)
  elif call == 'Commit':
    execute_reserved_hooks()
  elif call == 'Rollback' or call == 'BeginTransaction':
    clear_reserved_hooks()
