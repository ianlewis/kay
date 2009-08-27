# -*- coding: utf-8 -*-

"""
Kay session middleware.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import base64
import datetime
import cPickle as pickle

from werkzeug.contrib import sessions
from werkzeug.exceptions import HTTPException
from google.appengine.ext import db
from google.appengine.api import memcache

from kay.conf import settings
from kay.utils.decorators import retry_on_timeout
from models import GAESession

import kay.sessions

class GAESessionStore(sessions.SessionStore):
  """
  A session store class with GAE Datastore backend.
  """
  def __init__(self, session_class=None, session_prefix=None):
    self.session_prefix = session_prefix or settings.SESSION_PREFIX
    super(GAESessionStore, self).__init__(session_class)

  def get_key_name(self, sid):
    return '%s:%s' %(self.session_prefix ,sid)

  @retry_on_timeout(retries=5, secs=0.2)
  def save_to_db(self, key_name, session):
    gae_session = GAESession(
      key_name = key_name,
      data = self.encode(dict(session)),
      expire_date = (datetime.datetime.now() +
                     datetime.timedelta(seconds=settings.COOKIE_AGE))
    )
    gae_session.put()
    return gae_session

  def save(self, session):
    key_name = self.get_key_name(session.sid)
    gae_session = self.save_to_db(key_name, session)
    memcache.set(key_name, gae_session, settings.SESSION_MEMCACHE_AGE)

  @retry_on_timeout(retries=5, secs=0.2)
  def delete(self, session):
    s = GAESession.get_by_key_name(self.get_key_name(session.sid))
    if s:
      s.delete()

  @retry_on_timeout(retries=5, secs=0.2)
  def get(self, sid):
    key_name = self.get_key_name(sid)
    s = memcache.get(key_name)
    if s is None:
      s = GAESession.get_by_key_name(key_name)
    if not self.is_valid_key(sid) or s is None:
      return self.new()
    else:
      data = self.decode(s.data)
    return self.session_class(data, sid, False)
    
  def encode(self, session):
    "Returns the given session instance pickled and encoded as a string."
    pickled = pickle.dumps(session, pickle.HIGHEST_PROTOCOL)
    return base64.encodestring(pickled)

  def decode(self, session_data):
    encoded_data = base64.decodestring(session_data)
    try:
      return pickle.loads(encoded_data)
    # Unpickling can cause a variety of exceptions. If something happens,
    # just return an empty dictionary (an empty session).
    except:
      return {}


class SessionMiddleware(object):

  def __init__(self):
    self.session_store = GAESessionStore()

  def process_view(self, request, view_func, **kwargs):
    if hasattr(view_func, kay.sessions.NO_SESSION):
      return None
    sid = request.cookies.get(settings.COOKIE_NAME)
    if sid is None:
      request.session = self.session_store.new()
    else:
      request.session = self.session_store.get(sid)
    return None

  def process_response(self, request, response):
    if hasattr(request, 'session') and request.session.should_save:
      self.session_store.save(request.session)
      if not isinstance(response, HTTPException):
        response.set_cookie(settings.COOKIE_NAME, request.session.sid,
                            max_age=settings.COOKIE_AGE)
    return response
