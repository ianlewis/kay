# -*- coding: utf-8 -*-

"""
Views of Kay internal applications.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging

from werkzeug import Response

# TODO implement

def cron_frequent(request):
  logging.debug("cron frequent handler called.")
  return Response("OK")

def cron_hourly(request):
  logging.debug("cron hourly handler called.")
  return Response("OK")

