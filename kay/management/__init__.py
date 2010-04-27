# -*- coding: utf-8 -*-

"""
kay.management

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.

Taken from django.
"""


import sys
import os

from werkzeug.utils import import_string

from kay.management.shell import (
  rshell, shell, clear_datastore, create_user,
)
from kay.management.runserver import runserver_passthru_argv
from kay.management.startapp import startapp
from kay.management.startapp import startproject
from kay.management.appcfg import do_appcfg_passthru_argv
from kay.management.bulkloader import (
  do_bulkloader_passthru_argv, dump_all, restore_all,
)
from kay.management.test import do_runtest
from kay.management.preparse import do_preparse_bundle
from kay.management.preparse import do_preparse_apps
from kay.management.extract_messages import do_extract_messages
from kay.management.add_translations import do_add_translations
from kay.management.update_translations import do_update_translations
from kay.management.compile_translations import do_compile_translations
from kay.management.wxadmin import do_wxadmin
from kay.management.compile_media import do_compile_media

from kay.conf import settings

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

additional_actions = []

for app in settings.INSTALLED_APPS:
  try:
    appmod = import_string(app)
    if not os.path.exists(os.path.join(os.path.dirname(appmod.__file__),
                                       'management.py')):
      continue
    management_mod = import_string("%s.management" % app)
    for name, val in vars(management_mod).iteritems():
      if name.startswith("action_"):
        locals()[name] = getattr(management_mod, name)
        additional_actions.append(name)
  except Exception, e:
    import traceback
    sys.stderr.write('\n'.join(traceback.format_exception(*(sys.exc_info()))))
    pass

__all__ = [
  'runserver_passthru_argv', 'startapp', 'do_appcfg_passthru_argv',
  'do_bulkloader_passthru_argv', 'do_runtest', 'do_preparse_bundle',
  'do_extract_messages', 'do_add_translations', 'do_update_translations',
  'do_compile_translations', 'shell', 'rshell', 'do_preparse_apps',
  'startproject', 'do_wxadmin', 'clear_datastore', 'create_user', 'dump_all',
  'restore_all', 'do_compile_media',

  'action_dump_all', 'action_restore_all', 'action_shell', 'action_rshell',
  'action_startapp', 'action_startproject', 'action_test',
  'action_preparse_bundle', 'action_preparse_apps', 'action_extract_messages',
  'action_add_translations', 'action_update_translations',
  'action_compile_translations', 'action_appcfg', 'action_runserver',
  'action_bulkloader', 'action_clear_datastore', 'action_create_user',
  'action_wxadmin', 'action_compile_media',
] + additional_actions

def print_status(msg):
  print(msg)
  sys.stdout.flush()
