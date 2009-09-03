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

def maintenance_check(view):
  """
  Checks the request method is in one of the given methods
  """
  import logging
  from google.appengine.api.capabilities import CapabilitySet
  from werkzeug import Response
  from kay.utils import render_to_string
  from kay.i18n import gettext as _

  def wrapped(request, *args, **kwargs):
    datastore_write = CapabilitySet('datastore_v3', capabilities=['write'])
    datastore_writable = datastore_write.will_remain_enabled_for(60)
    if not datastore_writable:
      logging.warn('Datastore is not writable. %s' %
                   datastore_write.admin_message())
      if request.is_xhr:
        return ServiceUnavailable('Appengine might be under maintenance.')
      else:
        # Saving session will also fail.
        if hasattr(request, 'session'):
          del(request.session)
        return Response(
          render_to_string(
            "_internal/maintenance.html",
            {"message": _('Appengine might be under maintenance.')}),
          status=503)
        return redirect(reverse('_internal/maintenance_page'))
    return view(request, *args, **kwargs)
  return wrapped
