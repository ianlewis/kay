# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
Kay test management commands.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import logging
import os
import sys
import unittest

g_path = "/usr/local/google_appengine"
extra_path = [
  os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
  g_path,
  os.path.join(g_path, 'lib', 'antlr3'),
  os.path.join(g_path, 'lib', 'webob'),
  os.path.join(g_path, 'lib', 'django'),
  os.path.join(g_path, 'lib', 'yaml', 'lib'),
]
sys.path = extra_path + sys.path
APP_ID = u'test'
os.environ['APPLICATION_ID'] = APP_ID

import kay
kay.setup()

from google.appengine.ext import db
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub
from google.appengine.api import mail_stub
from google.appengine.api import urlfetch_stub
from google.appengine.api.memcache import memcache_stub
from google.appengine.api import user_service_stub

from kay.conf import settings
from kay.utils.importlib import import_module

def setup_stub():
  apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
  stub = datastore_file_stub.DatastoreFileStub('test','/dev/null',
                                               '/dev/null')
  apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)

  apiproxy_stub_map.apiproxy.RegisterStub(
    'user', user_service_stub.UserServiceStub())

  apiproxy_stub_map.apiproxy.RegisterStub(
    'memcache', memcache_stub.MemcacheServiceStub())


def runtest(target='', verbosity=0):
  suite = unittest.TestSuite()
  if target:
    tests_mod = import_module("%s.tests" % target)
    suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(
        tests_mod))
  else:
    for app_name in settings.INSTALLED_APPS:
      try:
        tests_mod = import_module("%s.tests" % app_name)
      except ImportError:
        logging.debug("Loading module %s.tests failed." % app_name)
      else:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(
            tests_mod))
  unittest.TextTestRunner(verbosity=verbosity).run(suite)

def runtest_passthru_argv(target='',verbosity=("v", 0)):
  setup_stub()
  runtest(target, verbosity)

