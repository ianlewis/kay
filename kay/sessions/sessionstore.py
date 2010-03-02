# -*- coding: utf-8 -*-

"""
Kay sessionstore.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging
import base64
import datetime
import cPickle as pickle

from werkzeug.contrib import (
  sessions, securecookie
)
from google.appengine.ext import db
from google.appengine.api import memcache

from kay.conf import settings
from kay.utils.decorators import retry_on_timeout
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
      try:
        s = GAESession.get_by_key_name(key_name)
      except db.BadValueError, e:
        logging.warn("get_by_key_name failed with db.BadValueError: %s" % e)
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
    except Exception:
      return {}

  def get_data(self, session):
    return session.sid


class SecureCookieSessionStore(object):
  """
  A session store class with GAE Datastore backend.
  """
  def __init__(self, session_prefix=None, secret_key=None):
    self.session_prefix = session_prefix or settings.SESSION_PREFIX
    self.secret_key = secret_key or settings.SECRET_KEY
  
  def new(self):
    return securecookie.SecureCookie(secret_key=self.secret_key)

  def get(self, data):
    return securecookie.SecureCookie.unserialize(data, self.secret_key)

  def save(self, session):
    pass

  def get_data(self, session):
    return session.serialize()

  def delete(self, session):
    return True
