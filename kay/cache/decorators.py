# -*- coding: utf-8 -*-

"""
Kay cache decorators

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import kay.cache

def no_cache(func):
  """
  This is a decortor for marking particular view not to cache.
  """
  setattr(func, kay.cache.NO_CACHE, True)
  return func
