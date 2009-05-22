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
from kay.management.rshell import (
  make_remote_shell, create_useful_locals_for_rshell, shell
)
from kay.management.runserver import (
  runserver, runserver_passthru_argv,
)
from kay.management.startapp import startapp
from kay.management.appcfg import (
  do_appcfg, do_appcfg_passthru_argv
)

action_shell = shell
action_rshell = make_remote_shell(create_useful_locals_for_rshell)
action_startapp = startapp

if __name__ == '__main__':
  if sys.argv[1] == "runserver":
    runserver_passthru_argv()
  elif sys.argv[1] == "appcfg":
    do_appcfg_passthru_argv()
  else:
    script.run()
