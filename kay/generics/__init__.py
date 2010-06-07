# -*- coding: utf-8 -*-

"""
Kay generics.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from kay.exceptions import NotAuthorized

OP_LIST = 'list'
OP_SHOW = 'show'
OP_CREATE = 'create'
OP_UPDATE = 'update'
OP_DELETE = 'delete'

# presets for authorization

def login_required(self, request, operation, obj=None, model_name=None,
                   prop_name=None):
  if request.user.is_anonymous():
    raise NotAuthorized()

def admin_required(self, request, operation, obj=None, model_name=None,
                   prop_name=None):
  if not request.user.is_admin:
    raise NotAuthorized()

def only_admin_can_write(self, request, operation, obj=None, model_name=None,
                         prop_name=None):
  if operation == OP_CREATE or operation == OP_UPDATE or \
        operation == OP_DELETE:
    if not request.user.is_admin:
      raise NotAuthorized()

def only_owner_can_write(self, request, operation, obj=None, model_name=None,
                         prop_name=None):
  if operation == OP_CREATE:
    if request.user.is_anonymous():
      raise NotAuthorized()
  elif operation == OP_UPDATE or operation == OP_DELETE:
    if self.owner_attr:
      owner = getattr(obj, self.owner_attr)
    else:
      owner = None
      for key, val in obj.fields().iteritems():
        if isinstance(val, OwnerProperty):
          owner = getattr(obj, key)
      if owner is None:
        raise NotAuthorized()
    if owner != request.user:
      raise NotAuthorized()

def only_owner_can_write_except_for_admin(self, request, operation, obj=None,
                                          model_name=None, prop_name=None):
  if request.user.is_admin:
    return True
  else:
    return only_owner_can_write(self, request, operation, obj)
