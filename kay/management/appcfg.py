# -*- coding: utf-8 -*-

"""
Kay appcfg management command.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import os
import sys
from os import listdir, path, mkdir

import kay
import kay.app
from kay.utils import local
from kay.utils.jinja2utils.compiler import compile_dir
from kay.utils.importlib import import_module
from kay.management.preparse import do_preparse_apps

def do_appcfg_passthru_argv():
  """
  Execute appcfg.py with specified parameters. For more details,
  please invoke 'python manage.py appcfg --help'.
  """
  from google.appengine.tools import appcfg
  progname = sys.argv[0]
  if len(sys.argv) < 3:
    sys.stderr.write('action required.\n')
    sys.exit(1)
  if sys.argv[2] == 'update':
    do_preparse_apps()
  sys.modules['__main__'] = appcfg
  
  args = sys.argv[2:]
  if "--help" in args:
    args = [progname] + args
  else:
    args = [progname] + args + [os.getcwdu()]
  appcfg.main(args)
  from kay.conf import settings
  if settings.PROFILE and sys.argv[2] == 'update':
    print '--------------------------\n' \
        'WARNING: PROFILER ENABLED!\n' \
        '--------------------------'
    
do_appcfg_passthru_argv.passthru = True
