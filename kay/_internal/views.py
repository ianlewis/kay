# -*- coding: utf-8 -*-

"""
Views of Kay internal applications.

:Copyright: (c) 2009 Accense Technology, Inc.,
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging

from werkzeug import Response

from kay.utils import render_to_response
from kay.sessions.decorators import no_session
from kay.i18n import gettext as _

# TODO implement

@no_session
def cron_frequent(request):
  logging.debug("cron frequent handler called.")
  return Response("OK")

@no_session
def cron_hourly(request):
  logging.debug("cron hourly handler called.")
  return Response("OK")

@no_session
def maintenance_page(request, message=_('Now it\'s under maintenance.')):
  return render_to_response("_internal/maintenance.html",
                            {"message": message})
