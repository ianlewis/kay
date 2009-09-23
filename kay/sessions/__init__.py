# -*- coding: utf-8 -*-

"""
Kay application for sessions.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

NO_SESSION = 'nosession'

def renew_session(request):
  from middleware import GAESessionStore
  session_store = GAESessionStore()
  oldsession = request.session
  request.session = session_store.new()
  # TODO: more efficiently
  for key, val in oldsession.iteritems():
    request.session[key] = val
  session_store.delete(oldsession)

