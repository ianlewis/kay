# -*- coding: utf-8 -*-

"""
kay.utils.decorators
~~~~~~~~~~~~~~~~~~~~

This module implements useful decorators for appengine datastore.

:Copyright: (c) 2009 Accense Technology, Inc.,
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     Ian Lewis <IanMLewis@gmail.com>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

DATASTORE_WRITABLE = "appengine_datastore_writable"

def retry_on_timeout(retries=3, secs=1):
  """A decorator to retry a given function performing db operations."""
  import time
  import logging
  from google.appengine.ext import db
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

def datastore_writable_for_certain_time():
  from google.appengine.api.capabilities import CapabilitySet
  from google.appengine.api import memcache
  datastore_writable = memcache.get(DATASTORE_WRITABLE)
  if datastore_writable is None:
    datastore_write = CapabilitySet('datastore_v3', capabilities=['write'])
    datastore_writable = datastore_write.will_remain_enabled_for(60)
    memcache.set(DATASTORE_WRITABLE, datastore_writable, 30)
  return datastore_writable

def maintenance_check(view):
  """
  Checks the request method is in one of the given methods
  """
  import logging
  from werkzeug import redirect
  from kay.utils import reverse
  def wrapped(request, *args, **kwargs):
    if not datastore_writable_for_certain_time():
      if request.is_xhr:
        # Ignore ajax request. This will cause 50? Status eventually.
        logging.debug('Datastore is not writable against an ajax request.')
      else:
        return redirect(reverse('_internal/maintenance_page'))
    return view(request, *args, **kwargs)
  return wrapped
