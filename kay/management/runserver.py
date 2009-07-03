# -*- coding: utf-8 -*-
#
# Copyright 2008 Google Inc.
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

"""
Kay runserver management commands.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import os
import sys

from kay.misc import get_datastore_paths

def args_have_option(args, option):
  for arg in args:
    if arg.startswith(option):
      return True
  return False

def runserver_passthru_argv():
  """
  Execute dev_appserver with appropriate parameters. For more details,
  please invoke 'python manage.py runserver --help'.
  """
  from google.appengine.tools import dev_appserver_main
  progname = sys.argv[1]
  args = []
  # hack __main__ so --help in dev_appserver_main works OK.
  sys.modules['__main__'] = dev_appserver_main    
  args.extend(sys.argv[2:])

  p = get_datastore_paths()
  if not args_have_option(args, "--datastore_path"):
    args.extend(["--datastore_path", p[0]])
  if not args_have_option(args, "--history_path"):
    args.extend(["--history_path", p[1]])
  # Append the current working directory to the arguments.
  dev_appserver_main.main([progname] + args + [os.getcwdu()])

runserver_passthru_argv.passthru = True
