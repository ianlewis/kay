# -*- coding: utf-8 -*-

"""
Kay session middleware.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import kay.sessions
from kay.conf import settings
from werkzeug import import_string

class SessionMiddleware(object):

  def __init__(self):
    session_store = import_string(settings.SESSION_STORE)
    self.session_store = session_store()

  def process_view(self, request, view_func, **kwargs):
    if hasattr(view_func, kay.sessions.NO_SESSION):
      return None
    data = request.cookies.get(settings.COOKIE_NAME)
    if data is None:
      request.session = self.session_store.new()
    else:
      request.session = self.session_store.get(data)
    return None

  def process_response(self, request, response):
    if hasattr(request, 'session') and request.session.should_save and \
          hasattr(response, 'set_cookie'):
      self.session_store.save(request.session)
      response.set_cookie(settings.COOKIE_NAME,
                          self.session_store.get_data(request.session),
                          max_age=settings.COOKIE_AGE)
    return response
