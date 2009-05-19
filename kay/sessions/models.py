# -*- coding: utf-8 -*-
"""
Kay session middleware
"""

import base64
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

from kay.conf import settings

class GAESession(db.Model):
  """
  A model for storing session.
  """
  data = db.TextProperty(required=True)
  expire_date = db.DateTimeProperty(required=True)

  def get_decoded(self):
    encoded_data = base64.decodestring(self.data)
    pickled, tamper_check = encoded_data[:-32], encoded_data[-32:]
    if md5_constructor(pickled + settings.SECRET_KEY).hexdigest() != tamper_check:
      raise SuspiciousOperation, "User tampered with session cookie."
    try:
      return pickle.loads(pickled)
    # Unpickling can cause a variety of exceptions. If something happens,
    # just return an empty dictionary (an empty session).
    except:
      return {}

