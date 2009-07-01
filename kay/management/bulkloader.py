# -*- coding: utf-8 -*-

"""
Kay bulkload management command.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import os
import sys

from shell import get_all_models_as_dict

def do_bulkloader_passthru_argv():
  from google.appengine.tools import bulkloader
  progname = sys.argv[0]
  sys.modules['__main__'] = bulkloader
  models = get_all_models_as_dict()
  args = []
  for arg in sys.argv[1:]:
    if arg.startswith("--kind"):
      kind = arg[7:]
      model = models.get(kind, None)
      if model is None:
        print "Invalid kind: %s." % kind
        sys.exit(1)
      args.append("--kind=%s" % model.kind())
    else:
      args.append(arg)
  sys.exit(bulkloader.main(args))
