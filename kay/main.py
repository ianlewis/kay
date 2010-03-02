# -*- coding: utf-8 -*-

"""
Kay main handler script.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging
import os
import sys

import kay
kay.setup()

from kay.app import get_application
from kay.utils.handlers import KayHandler
from kay.conf import (
  settings, LazySettings
)

application = get_application()
debugged_application = None
applications = {}
debugged_applications = {}

def real_main():
  global application
  global applications
  server_name = os.environ.get('SERVER_NAME')
  target_setting = settings.PER_DOMAIN_SETTINGS.get(server_name, None)
  if target_setting:
    applications[server_name] = get_application(
      settings=LazySettings(settings_module=target_setting))
  if settings.DEBUG:
    logging.getLogger().setLevel(logging.DEBUG)
    if 'SERVER_SOFTWARE' in os.environ and \
          os.environ['SERVER_SOFTWARE'].startswith('Dev'):
      # use our debug.utils with Jinja2 templates
      import debug.utils
      sys.modules['werkzeug.debug.utils'] = debug.utils

      # don't use inspect.getsourcefile because the imp module is empty 
      import inspect
      inspect.getsourcefile = inspect.getfile
    
      # wrap the application
      from werkzeug import DebuggedApplication
      global debugged_application
      global debugged_applications
      if target_setting:
        if not debugged_applications.has_key(server_name):
          debugged_applications[server_name] = applications[server_name] = \
              DebuggedApplication(applications[server_name], evalex=True)
        else:
          applications[server_name] = debugged_applications[server_name]
      else:
        if debugged_application is None:
          debugged_application = application = DebuggedApplication(application,
                                                                   evalex=True)
        else:
          application = debugged_application
  else:
    logging.getLogger().setLevel(logging.INFO)
  if target_setting:
    KayHandler().run(applications[server_name])
  else:
    KayHandler().run(application)

def profile_main():
  # This is the main function for profiling 
  # We've renamed our original main() above to real_main()
  import cProfile, pstats
  prof = cProfile.Profile()
  prof = prof.runctx("real_main()", globals(), locals())
  print "<!--"
  print "/*"
  print "-->"
  print "<pre>"
  stats = pstats.Stats(prof)
  stats.sort_stats("time")  # Or cumulative
  stats.print_stats(80)  # 80 = how many to print
  # The rest is optional.
  if settings.PRINNT_CALLEES_ON_PROFILING:
    stats.print_callees()
  if settings.PRINNT_CALLERS_ON_PROFILING:
    stats.print_callers()
  print "</pre>"
  print "<!--"
  print "*/"
  print "//-->"

if settings.PROFILE:
  main = profile_main
else:
  main = real_main

if __name__ == '__main__':
  main()
