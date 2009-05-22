# -*- coding: utf-8 -*-

"""
Kay appcfg management command.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import os
import sys

def do_appcfg_passthru_argv():
  from google.appengine.tools import appcfg
  progname = sys.argv[0]
  if len(sys.argv) < 3:
    sys.stderr.write('action required.\n')
    sys.exit(1)
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

def do_appcfg(action='', quiet=('q', False), verbose=('v', False), noisy=False,
              server=('s', 'appengine.google.com'), secure=False,
              email=('e', ''), cookies=True):
  from google.appengine.tools import appcfg
  progname = sys.argv[0]
  args = []
  if not action:
    sys.stderr.write('action required.\n')
    sys.exit(1)
  args.extend([action])
  if quiet:
    args.extend(["--quiet"])
  if verbose:
    args.extend(["--verbose"])
  if noisy:
    args.extend(["--noisy"])
  if server:
    args.extend(["--server", server])
  if secure:
    args.extend(["--secure"])
  if email:
    args.extend(["--email"])
  if not cookies:
    args.extend(["--no_cookies"])
  sys.modules['__main__'] = appcfg
  appcfg.main([progname] + args + [os.getcwdu()])
  from kay.conf import settings
  if settings.PROFILE and action == 'update':
    print '--------------------------\n' \
        'WARNING: PROFILER ENABLED!\n' \
        '--------------------------'

    
