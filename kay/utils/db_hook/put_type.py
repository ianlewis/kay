# -*- coding: utf-8 -*-

"""
Kay utils.db_hook.put_type module.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

NEWLY_CREATED = 1
UPDATED = 2
MAYBE_NEWLY_CREATED = 3
MAYBE_UPDATED = 4
UNKOWN = 5

type_names = {
  1: "Newly Created",
  2: "Updated",
  3: "Maybe Newly Created",
  4: "Maybe Updated",
  5: "Unkown",
}

def get_name(type):
  return type_names.get(type, None)