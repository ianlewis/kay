# -*- coding: utf-8 -*-

"""
kay.utils.decorators
~~~~~~~~~~~~~~~~~~~~

This module implements useful decorators for appengine datastore.

:copyright: (c) 2009 by Accense Technology, Inc. See AUTHORS for more
details.
:license: BSD, see LICENSE for more details.
"""

import time
import logging

from google.appengine.ext import db

def retry_on_timeout(retries=3, secs=1):
  """A decorator to retry a given function performing db operations."""
  def _decorator(func):
    def _wrapper(*args, **kwds):
      tries = 0
      while True:
        try:
          tries += 1
          return func(*args, **kwds)
        except db.Timeout, e:
          logging.debug(e)
          if tries > retries:
            raise e
          else:
            wait_secs = secs * tries ** 2
            logging.warning("Retrying function %r in %d secs" %
                            (func, wait_secs))
            time.sleep(wait_secs)
    return _wrapper
  return _decorator
