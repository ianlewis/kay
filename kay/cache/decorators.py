# -*- coding: utf-8 -*-

"""
Kay cache decorators

:Copyright: (c) 2009 Accense Technology, Inc.,
                     Takashi Matsuo <tmatsuo@candit.jp>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import kay.cache
from kay.utils.decorators import (
  decorator_from_middleware_with_args, decorator_from_middleware,
)
from kay.cache.middleware import CacheMiddleware

def no_cache(func):
  """
  This is a decortor for marking particular view not to cache.
  """
  setattr(func, kay.cache.NO_CACHE, True)
  return func

cache_page = decorator_from_middleware_with_args(CacheMiddleware)
