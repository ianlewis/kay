# -*- coding: utf-8 -*-

"""
Kay framework.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import sys

import kay.app

def print_status(msg='',nl=True):
  if nl:
    print(msg)
  else:
    print(msg),
  sys.stdout.flush()

def get_user_apps():
  ret = []
  # retrieve main app
  main_app = kay.app.get_application()
  apps = [main_app.app]
  for key, submount_app in main_app.mounts.iteritems():
    if not hasattr(submount_app, 'app_settings') or key == "/_kay":
      continue
    apps.append(submount_app)
  for app in apps:
    for user_app in app.app_settings.INSTALLED_APPS:
      if user_app.startswith("kay."):
        continue
      ret.append(user_app)
  return ret
    
