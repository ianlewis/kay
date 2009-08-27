#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Kay test base class.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import sys
import os
import unittest

from google.appengine.ext import db
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub
from google.appengine.api import mail_stub
from google.appengine.api import urlfetch_stub
from google.appengine.api.memcache import memcache_stub
from google.appengine.api import user_service_stub

from werkzeug import BaseResponse, Client, Request

import kay
from kay.app import get_application
from kay.utils import local
from kay.utils import forms
from kay.utils.forms import ValidationError

def get_env():
  env = dict(os.environ)
  env['wsgi.input'] = sys.stdin
  env['wsgi.errors'] = sys.stderr
  env['wsgi.version'] = "1.0"
  env['wsgi.run_once'] = True
  env['wsgi.url_scheme'] = 'http'
  env['wsgi.multithread']  = False
  env['wsgi.multiprocess'] = True
  return env

class TestCase(unittest.TestCase):

  def setUp(self):
    self.client = Client(get_application(), BaseResponse)
    self.c = self.client

  def tearDown(self):
    pass
