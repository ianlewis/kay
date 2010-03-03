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

__all__ = [
  'runserver_passthru_argv', 'startapp', 'do_appcfg_passthru_argv',
  'do_bulkloader_passthru_argv', 'do_runtest', 'do_preparse_bundle',
  'do_extract_messages', 'do_add_translations', 'do_update_translations',
  'do_compile_translations', 'shell', 'rshell', 'do_preparse_apps',
  'startproject', 'do_wxadmin', 'clear_datastore', 'create_user', 'dump_all',
  'restore_all', 'do_compile_media'
]

def print_status(msg):
  print(msg)
  sys.stdout.flush()
