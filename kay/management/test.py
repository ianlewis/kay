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

from google.appengine.tools import dev_appserver_main
from google.appengine.tools.dev_appserver_main import *

from kay.conf import settings
from kay.misc import get_datastore_paths

def passthru_argv():
  progname = sys.argv[0]
  args = []
  # hack __main__ so --help in dev_appserver_main works OK.
  sys.modules['__main__'] = dev_appserver_main
  args.extend(sys.argv[2:])

  p = get_datastore_paths()
  if not "--datastore_path" in args:
    args.extend(["--datastore_path", p[0]])
  if not "--history_path" in args:
    args.extend(["--history_path", p[1]])
  # Append the current working directory to the arguments.
  #dev_appserver_main.main([progname] + args + [os.getcwdu()])
  return [progname] + args + [os.getcwdu()]

def setup_stub(argv):
  args, option_dict = ParseArguments(argv)

  if len(args) != 1:
    print >>sys.stderr, 'Invalid arguments'
    PrintUsageExit(1)

  root_path = args[0]
  for suffix in ('yaml', 'yml'):
    path = os.path.join(root_path, 'app.%s' % suffix)
    if os.path.exists(path):
      api_version = SetPaths(path)
      break
  else:
    logging.error("Application configuration file not found in %s" % root_path)
    return 1

  SetGlobals()
  dev_appserver.API_VERSION = api_version

  if '_DEFAULT_ENV_AUTH_DOMAIN' in option_dict:
    auth_domain = option_dict['_DEFAULT_ENV_AUTH_DOMAIN']
    dev_appserver.DEFAULT_ENV['AUTH_DOMAIN'] = auth_domain
  if '_ENABLE_LOGGING' in option_dict:
    enable_logging = option_dict['_ENABLE_LOGGING']
    dev_appserver.HardenedModulesHook.ENABLE_LOGGING = enable_logging

  log_level = option_dict[ARG_LOG_LEVEL]
  port = option_dict[ARG_PORT]
  datastore_path = option_dict[ARG_DATASTORE_PATH]
  login_url = option_dict[ARG_LOGIN_URL]
  template_dir = option_dict[ARG_TEMPLATE_DIR]
  serve_address = option_dict[ARG_ADDRESS]
  require_indexes = option_dict[ARG_REQUIRE_INDEXES]
  allow_skipped_files = option_dict[ARG_ALLOW_SKIPPED_FILES]
  static_caching = option_dict[ARG_STATIC_CACHING]

  option_dict['root_path'] = os.path.realpath(root_path)

  logging.basicConfig(
    level=log_level,
    format='%(levelname)-8s %(asctime)s %(filename)s:%(lineno)s] %(message)s')

  config = None
  try:
    config, matcher = dev_appserver.LoadAppConfig(root_path, {})
  except yaml_errors.EventListenerError, e:
    logging.error('Fatal error when loading application configuration:\n' +
                  str(e))
    return 1
  except dev_appserver.InvalidAppConfigError, e:
    logging.error('Application configuration file invalid:\n%s', e)
    return 1

  if option_dict[ARG_ADMIN_CONSOLE_SERVER] != '':
    server = MakeRpcServer(option_dict)
    update_check = appcfg.UpdateCheck(server, config)
    update_check.CheckSupportedVersion()
    if update_check.AllowedToCheckForUpdates():
      update_check.CheckForUpdates()

  try:
    dev_appserver.SetupStubs(config.application, **option_dict)
  except:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    logging.error(str(exc_type) + ': ' + str(exc_value))
    logging.debug(''.join(traceback.format_exception(
          exc_type, exc_value, exc_traceback)))
    return 1

def runtest():
  suite = unittest.TestSuite()
  for app_name in settings.INSTALLED_APPS:
    try:
      tests_mod = __import__("%s.tests" % app_name, fromlist=[app_name])
    except ImportError:
      pass
    else:
      suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(tests_mod))
  unittest.TextTestRunner().run(suite)

def runtest_passthru_argv():
  setup_stub(passthru_argv())
  runtest()

