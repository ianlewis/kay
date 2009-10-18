# -*- coding: utf-8 -*-

"""
Kay application for sessions.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

NO_SESSION = 'nosession'

from werkzeug.utils import import_string
from kay.conf import settings

def _renew_session(request, copy_data=True):
  store_cls = import_string(settings.SESSION_STORE)
  session_store = store_cls()
  oldsession = request.session
  request.session = session_store.new()
  # TODO: more efficiently
  if copy_data:
    for key, val in oldsession.iteritems():
      request.session[key] = val
  else:
    request.session.modified = True
  session_store.delete(oldsession)

def renew_session(request):
  _renew_session(request)

def flush_session(request):
  _renew_session(request, copy_data=False)

class NoSessionMixin(object):
  nosession = True
