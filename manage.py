#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Kay management script.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
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

action_dump_all = dump_all
action_restore_all = restore_all
action_shell = shell
action_rshell = rshell
action_startapp = startapp
action_startproject = startproject
action_test = do_runtest
action_preparse_bundle = do_preparse_bundle
action_preparse_apps = do_preparse_apps
action_extract_messages = do_extract_messages
action_add_translations = do_add_translations
action_update_translations = do_update_translations
action_compile_translations = do_compile_translations
action_appcfg = do_appcfg_passthru_argv
action_runserver = runserver_passthru_argv
action_bulkloader = do_bulkloader_passthru_argv
action_clear_datastore = clear_datastore
action_create_user = create_user
action_wxadmin = do_wxadmin
action_compile_media = do_compile_media

if __name__ == '__main__':
  if len(sys.argv) == 1:
    sys.argv.append("--help")
  script.run()
