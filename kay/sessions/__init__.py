# -*- coding: utf-8 -*-

from middleware import GAESessionStore

def renew_session(request):
  session_store = GAESessionStore()
  oldsession = request.session
  request.session = session_store.new()
  for key, val in oldsession.iteritems():
    request.session[key] = val
  session_store.delete(oldsession)

