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
from kay.management.test import runtest_passthru_argv

action_shell = shell
action_rshell = rshell
action_startapp = startapp

action_runserver = runserver_passthru_argv
action_appcfg = do_appcfg_passthru_argv
action_bulkloader = do_bulkloader_passthru_argv
action_test = runtest_passthru_argv

script.run()
