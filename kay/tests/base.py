#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import kay
from werkzeug import Request

from kay.utils import local
from kay.utils import forms
from kay.utils.forms import ValidationError

class GAETestBase(unittest.TestCase):

  def get_env(self):
    env = dict(os.environ)
    env['wsgi.input'] = sys.stdin
    env['wsgi.errors'] = sys.stderr
    env['wsgi.version'] = "1.0"
    env['wsgi.run_once'] = True
    env['wsgi.url_scheme'] = 'http'
    env['wsgi.multithread']  = False
    env['wsgi.multiprocess'] = True
    return env
    
  def setUp(self):
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    stub = datastore_file_stub.DatastoreFileStub('test','/dev/null',
                                                 '/dev/null')
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)

    apiproxy_stub_map.apiproxy.RegisterStub(
      'user', user_service_stub.UserServiceStub())

    apiproxy_stub_map.apiproxy.RegisterStub(
      'memcache', memcache_stub.MemcacheServiceStub())
