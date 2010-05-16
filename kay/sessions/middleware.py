# -*- coding: utf-8 -*-

"""
Kay session middleware.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import kay.sessions
from kay.conf import settings
from werkzeug import import_string

class LazySession(object):
  def __get__(self, request, obj_type=None):
    session_store = import_string(settings.SESSION_STORE)()
    if not hasattr(request, '_cached_session'):
      data = request.cookies.get(settings.COOKIE_NAME)
      if data is None:
        request._cached_session = session_store.new()
      else:
        request._cached_session = session_store.get(data)
    return request._cached_session


class SessionMiddleware(object):

  def process_request(self, request):
    request.__class__.session = LazySession()

  def process_response(self, request, response):
    if hasattr(request, '_cached_session') and \
          request.session.should_save and hasattr(response, 'set_cookie'):
      session_store = import_string(settings.SESSION_STORE)()
      session_store.save(request.session)
      response.set_cookie(settings.COOKIE_NAME,
                          session_store.get_data(request.session),
                          max_age=settings.COOKIE_AGE)
    return response
