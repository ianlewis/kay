# -*- coding: utf-8 -*-

"""
Kay appcfg management command.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import os
import sys
import logging
from os import listdir, path, mkdir
import optparse

import kay
import kay.app
from kay.utils import local
from kay.utils.jinja2utils.compiler import compile_dir
from kay.management.preparse import do_preparse_apps
from kay.management.utils import print_status
from shell import get_all_models_as_dict

class HookedOptionParser(optparse.OptionParser):
  def get_prog_name(self):
    return "manage.py appcfg"
  
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
  if 'update' in sys.argv:
    do_preparse_apps()
  
  models = get_all_models_as_dict()
  args = []
  for arg in sys.argv[2:]:
    args.append(arg)
    if arg == "request_logs":
      args.append(os.getcwdu())

  if "--help" in args or "help" in args or "request_logs" in args:
    args = [progname] + args
  else:
    args = [progname] + args + [os.getcwdu()]
  logging.basicConfig(format=('%(asctime)s %(levelname)s %(filename)s:'
                              '%(lineno)s %(message)s '))
  try:
    app = appcfg.AppCfgApp(args, parser_class=HookedOptionParser)
    result = app.Run()
    if result:
      sys.exit(result)
  except KeyboardInterrupt:
    print_status('Interrupted.')
    sys.exit(1)
  from kay.conf import settings
  if settings.PROFILE and 'update' in sys.argv:
    print_status(
      '--------------------------\n'
      'WARNING: PROFILER ENABLED!\n'
      '--------------------------'
    )

    
do_appcfg_passthru_argv.passthru = True
