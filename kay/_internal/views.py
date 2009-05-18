# -*- coding: utf-8 -*-

import logging
import datetime

from werkzeug import Response

import settings
from kay import utils

batch_num = 30

def cron_frequent(request):
  logging.debug("cron frequent handler called.")
  return Response("OK")

def cron_hourly(request):
  logging.debug("cron hourly handler called.")
  if utils.use_session():
    from google.appengine.ext import db
    from kay.middleware.session import GAESession
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

