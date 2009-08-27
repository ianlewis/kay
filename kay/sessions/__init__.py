# -*- coding: utf-8 -*-

"""
Kay application for sessions.

:copyright: (c) 2009 by Accense Technology, Inc. See AUTHORS for more
details.
:license: BSD, see LICENSE for more details.
"""

from middleware import GAESessionStore

NO_SESSION = 'nosession'

def renew_session(request):
  session_store = GAESessionStore()
  oldsession = request.session
  request.session = session_store.new()
  for key, val in oldsession.iteritems():
    request.session[key] = val
  session_store.delete(oldsession)

