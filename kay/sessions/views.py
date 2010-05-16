# -*- coding: utf-8 -*-

"""
Kay sessions views..

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging
import datetime

from werkzeug import Response

from kay.conf import settings

batch_num = 30

def use_session():
  return 'kay.sessions.middleware.SessionMiddleware' in \
      settings.MIDDLEWARE_CLASSES

def purge_old_sessions(request):
  if use_session():
    from google.appengine.ext import db
    from kay.sessions.models import GAESession
    now = datetime.datetime.now()
    entries = db.Query(GAESession, keys_only=True).filter(
      'expire_date <', now).fetch(batch_num)
    while len(entries) > 0:
      logging.debug("Now deleting %d entries." % len(entries))
      db.delete(entries)
      entries = db.Query(GAESession, keys_only=True).filter(
      'expire_date <', now).fetch(batch_num)
    logging.debug("Finished deleting expired sessions.")

  return Response("OK")
