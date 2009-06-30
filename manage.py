#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Kay management script.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import sys
import os
import logging

sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path
import kay
kay.setup_env(manage_py_env=True)
from werkzeug import script
from kay.management.shell import (
  rshell, shell
)
from kay.management.runserver import (
  runserver, runserver_passthru_argv,
)
from kay.management.startapp import startapp
from kay.management.appcfg import (
  do_appcfg, do_appcfg_passthru_argv,
)
from kay.management.bulkloader import do_bulkloader_passthru_argv
from kay.management.test import do_runtest
from kay.management.preparse_bundle import do_preparse_bundle

action_shell = shell
action_rshell = rshell
action_startapp = startapp
action_test = do_runtest
action_preparse_bundle = do_preparse_bundle

if __name__ == '__main__':
  if len(sys.argv) == 1:
    sys.argv.append("--help")
    script.run()
  elif sys.argv[1] == "runserver":
    runserver_passthru_argv()
  elif sys.argv[1] == "appcfg":
    do_appcfg_passthru_argv()
  elif sys.argv[1] == "bulkloader":
    do_bulkloader_passthru_argv()
  else:
    script.run()
