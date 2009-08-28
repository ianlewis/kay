# -*- coding: utf-8 -*-

"""
Kay bulkload management command.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import os
import sys

from kay.management.utils import print_status
from shell import get_all_models_as_dict

def do_bulkloader_passthru_argv():
  """
  Execute bulkloader script with appropriate parameters. For more
  details, please invoke 'python manage.py bulkloader --help'.
  """
  from google.appengine.tools import bulkloader
  progname = sys.argv[0]
  models = get_all_models_as_dict()
  args = []
  for arg in sys.argv[1:]:
    if arg.startswith("--kind="):
      kind = arg[7:]
      model = models.get(kind, None)
      if model is None:
        print_status("Invalid kind: %s." % kind)
        sys.exit(1)
      args.append("--kind=%s" % model.kind())
    else:
      args.append(arg)
  if '--help' in args:
    print_status(bulkloader.__doc__ % {'arg0': "manage.py bulkloader"})
    sys.stdout.flush()
    sys.stderr.flush()
    sys.exit(0)
    
  sys.exit(bulkloader.main(args))

do_bulkloader_passthru_argv.passthru = True
