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


import os
import sys

from kay.misc import get_datastore_paths

def start_dev_appserver(clear_datastore=('c', False), addr=('a', ''),
                        port=('p', 8000), datastore_path='',
                        history_path='', smtp_host='', smtp_port=0,
                        enable_sendmail=False):
  """Starts the appengine dev_appserver program for the Django project.

  The appserver is run with default parameters. If you need to pass any special
  parameters to the dev_appserver you will have to invoke it manually.
  """
  from google.appengine.tools import dev_appserver_main
  progname = sys.argv[0]
  args = []
  # hack __main__ so --help in dev_appserver_main works OK.
  sys.modules['__main__'] = dev_appserver_main

  if clear_datastore:
    args.extend(["-c"])
  if addr:
    args.extend(["--address", addr])
  if port:
    args.extend(["--port", port])
  p = get_datastore_paths()
  if not datastore_path:
    args.extend(["--datastore_path", p[0]])
  else:
    args.extend(["--datastore_path", datastore_path])
  if not history_path:
    args.extend(["--history_path", p[1]])
  else:
    args.extend(["--history_path", history_path])
  if smtp_host:
    args.extend(["--smtp_host", smtp_host])
  if smtp_port:
    args.extend(["--smtp_port", smtp_port])
  if enable_sendmail:
    args.extend(["--enable_sendmail"])

  # Append the current working directory to the arguments.
  dev_appserver_main.main([progname] + args + [os.getcwdu()])
