# -*- coding: utf-8 -*-

"""
Kay session model.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import base64
import cPickle as pickle
import hashlib
md5_constructor = hashlib.md5
sha_constructor = hashlib.sha1

from werkzeug.contrib import sessions
from google.appengine.ext import db

from kay.exceptions import SuspiciousOperation
from kay.conf import settings

class GAESession(db.Model):
  """
  A model for storing session.
  """
  data = db.TextProperty(required=True)
  expire_date = db.DateTimeProperty(required=True)

