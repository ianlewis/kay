# -*- coding: utf-8 -*-

"""
Kay application for sessions.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from middleware import GAESessionStore

def renew_session(request):
  session_store = GAESessionStore()
  oldsession = request.session
  request.session = session_store.new()
  for key, val in oldsession.iteritems():
    request.session[key] = val
  session_store.delete(oldsession)

