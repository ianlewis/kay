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

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import os
import sys

from kay.misc import get_datastore_paths
from kay.management.utils import print_status

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
  progname = "manage.py runserver"
  args = []
  args.extend(sys.argv[2:])

  p = get_datastore_paths()
  if not args_have_option(args, "--datastore_path"):
    args.extend(["--datastore_path", p[0]])
  if not args_have_option(args, "--history_path"):
    args.extend(["--history_path", p[1]])
  # Append the current working directory to the arguments.
  if "-h" in args or "--help" in args:
    render_dict = dev_appserver_main.DEFAULT_ARGS.copy()
    render_dict['script'] = "manage.py runserver"
    print_status(dev_appserver_main.__doc__ % render_dict)
    sys.stdout.flush()
    sys.exit(0)
    
  dev_appserver_main.main([progname] + args + [os.getcwdu()])

runserver_passthru_argv.passthru = True
