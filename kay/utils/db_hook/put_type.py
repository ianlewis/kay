# -*- coding: utf-8 -*-

"""
Kay utils.db_hook.put_type module.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

NEWLY_CREATED = 1
UPDATED = 2
MAYBE_NEWLY_CREATED = 3
MAYBE_UPDATED = 4
UNKNOWN = 5

type_names = {
  1: "Newly Created",
  2: "Updated",
  3: "Maybe Newly Created",
  4: "Maybe Updated",
  5: "Unknown",
}

def get_name(type):
  return type_names.get(type, None)
