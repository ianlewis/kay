# -*- coding: utf-8 -*-

import os
import sys

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

    
