# -*- coding: utf-8 -*-
"""
Kay session middleware
"""

import settings
import base64
import datetime
import cPickle as pickle
try:
  import hashlib
  md5_constructor = hashlib.md5
  sha_constructor = hashlib.sha1
except ImportError:
  import md5
  md5_constructor = md5.new
  import sha
  sha_constructor = sha.new

from werkzeug.contrib import sessions
from google.appengine.ext import db

from models import GAESession


class GAESessionStore(sessions.SessionStore):
  """
  A session store class with GAE Datastore backend.
  """
  def __init__(self, session_class=None, session_prefix=None):
    self.session_prefix = session_prefix or settings.SESSION_PREFIX
    super(GAESessionStore, self).__init__(session_class)

  def get_key_name(self, sid):
    return '%s:%s' %(self.session_prefix ,sid)

  def save(self, session):
    GAESession(key_name = self.get_key_name(session.sid),
               data = self.encode(dict(session)),
               expire_date = (datetime.datetime.now() +
                              datetime.timedelta(seconds=settings.COOKIE_AGE))
    ).put()

  def delete(self, session):
    s = GAESession.get_by_key_name(self.get_key_name(session.sid))
    if s:
      s.delete()

  def get(self, sid):
    s = GAESession.get_by_key_name(self.get_key_name(sid))
    if not self.is_valid_key(sid) or s is None:
      return self.new()
    else:
      data = self.decode(s.data)
    return self.session_class(data, sid, False)
    
  def encode(self, session):
    "Returns the given session instance pickled and encoded as a string."
    pickled = pickle.dumps(session, pickle.HIGHEST_PROTOCOL)
    pickled_md5 = md5_constructor(pickled + settings.SECRET_KEY).hexdigest()
    return base64.encodestring(pickled + pickled_md5)

  def decode(self, session_data):
    encoded_data = base64.decodestring(session_data)
    pickled, tamper_check = encoded_data[:-32], encoded_data[-32:]
    if md5_constructor(pickled + settings.SECRET_KEY).hexdigest() != tamper_check:
      raise SuspiciousOperation("User tampered with session cookie.")
    try:
      return pickle.loads(pickled)
    # Unpickling can cause a variety of exceptions. If something happens,
    # just return an empty dictionary (an empty session).
    except:
      return {}


class SessionMiddleware(object):

  def __init__(self):
    """
    TODO: Add a capability to set various cookie settings.
    """
    self.session_store = GAESessionStore()

  def process_request(self, request):
    sid = request.cookies.get(settings.COOKIE_NAME)
    if sid is None:
      request.session = self.session_store.new()
    else:
      request.session = self.session_store.get(sid)
    return None

  def process_response(self, request, response):
    if request.session.should_save:
      self.session_store.save(request.session)
      response.set_cookie(settings.COOKIE_NAME, request.session.sid,
                          max_age=settings.COOKIE_AGE)
    return response
