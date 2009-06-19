# -*- coding: utf-8 -*-

"""
Kay bulkload management command.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import os
import sys

def do_bulkloader_passthru_argv():
  from google.appengine.tools import bulkloader
  progname = sys.argv[0]
  sys.modules['__main__'] = bulkloader

  args = sys.argv[1:]
  sys.exit(bulkloader.main(args))
