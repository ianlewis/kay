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
from kay.management.rshell import make_remote_shell, init_remote_shell
from kay.management.runserver import start_dev_appserver
from kay.management.startapp import startapp
from kay.management.appcfg import do_appcfg

action_shell = script.make_shell()
action_rshell = make_remote_shell(init_remote_shell)
action_runserver = start_dev_appserver
action_appcfg = do_appcfg
action_startapp = startapp

if __name__ == '__main__':
  script.run()

