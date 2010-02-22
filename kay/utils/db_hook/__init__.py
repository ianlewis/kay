# -*- coding: utf-8 -*-

"""
Kay utils.db_hook module.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import datetime

from google.appengine.api import datastore
from google.appengine.ext import db

from kay.utils import local

import put_type

pre_save_hooks = {}
pre_delete_hooks = {}
post_save_hooks = {}

def register_pre_save_hook(func, model):
  global pre_save_hooks
  kind = model.kind()
  func_list = pre_save_hooks.get(kind, [])
  func_list.append(func)
  pre_save_hooks[kind] = func_list

def register_pre_delete_hook(func, model):
  global pre_delete_hooks
  kind = model.kind()
  func_list = pre_delete_hooks.get(kind, [])
  func_list.append(func)
  pre_delete_hooks[kind] = func_list

def register_post_save_hook(func, model):
  global post_save_hooks
  kind = model.kind()
  func_list = post_save_hooks.get(kind, [])
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

def execute_post_save_hooks(kind, key, entity):
  put_type_id = put_type.UNKNOWN
  func_list = post_save_hooks.get(kind, None)
  if func_list is not None:
    last_path = entity.key().path().element_list()[-1]
    has_name = last_path.has_name()
    if last_path.has_id():
      if last_path.id() == 0:
        key_auto_generated = True
        put_type_id = put_type.NEWLY_CREATED
      else:
        key_auto_generated = False
    entity.key_.CopyFrom(key)
    e = datastore.Entity._FromPb(entity)
    instance = db.class_for_kind(kind).from_entity(e)
    if has_name or not key_auto_generated:
      created = get_created_datetime(instance)
      updated = get_updated_datetime(instance)
      if created:
        threshold = datetime.timedelta(0,0,1500)
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
      tmp_list = getattr(local, '_reserved_hooks', [])
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

def kind_name_from_key(key):
  return key.path().element_list()[-1].type()

def post_hook(service, call, request, response):
  if call == 'Put':
    for key, entity in zip(response.key_list(), request.entity_list()):
      kind = kind_name_from_key(key)
      execute_post_save_hooks(kind, key, entity)
  elif call == 'Commit':
    execute_reserved_hooks()
  elif call == 'Rollback' or call == 'BeginTransaction':
    clear_reserved_hooks()

def execute_pre_save_hooks(kind, pb_key, entity):
  put_type_id = put_type.UNKNOWN
  func_list = pre_save_hooks.get(kind, None)
  if func_list is not None:
    key = db.Key._FromPb(pb_key)
    if not key.id_or_name():
      path = key.to_path()[:-1]
      path.append(1)
      model_key = db.Key.from_path(*path)
      ids = datastore.AllocateIds(model_key, 1)
      path = path[:-1]
      path.append(ids[0])
      new_key = db.Key.from_path(*path)
      pb_key = new_key._ToPb()
      entity.key().CopyFrom(pb_key)
      group = entity.mutable_entity_group()
      root = entity.key().path().element(0)
      group.add_element().CopyFrom(root)
      e = datastore.Entity._FromPb(entity)
      instance = db.class_for_kind(kind).from_entity(e)
      put_type_id = put_type.NEWLY_CREATED
    else:
      entity.key_.CopyFrom(pb_key)
      e = datastore.Entity._FromPb(entity)
      instance = db.class_for_kind(kind).from_entity(e)
      created = get_created_datetime(instance)
      updated = get_updated_datetime(instance)
      if created:
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
    for func in func_list:
      func(instance, put_type_id)

def execute_pre_delete_hooks(kind, pb_key):
  func_list = pre_delete_hooks.get(kind, None)
  key = db.Key._FromPb(pb_key)
  if func_list is not None:
    for func in func_list:
      func(key)

def pre_hook(service, call, request, response):
  if call == 'Put':
    for entity in request.entity_list():
      pb_key = entity.key()
      kind = kind_name_from_key(pb_key)
      execute_pre_save_hooks(kind, pb_key, entity)
  elif call == 'Delete':
    for pb_key in request.key_list():
      kind = kind_name_from_key(pb_key)
      execute_pre_delete_hooks(kind, pb_key)
