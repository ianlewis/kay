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
from kay.management import *

action_shell = shell
action_rshell = rshell
action_startapp = startapp
action_test = do_runtest
action_preparse_bundle = do_preparse_bundle
action_extract_messages = do_extract_messages
action_add_translations = do_add_translations
action_update_translations = do_update_translations
action_compile_translations = do_compile_translations
action_appcfg = do_appcfg_passthru_argv
action_runserver = runserver_passthru_argv
action_bulkloader = do_bulkloader_passthru_argv

if __name__ == '__main__':
  if len(sys.argv) == 1:
    sys.argv.append("--help")
  script.run()
