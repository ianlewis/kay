# -*- coding: utf-8 -*-

"""
Kay framework.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import sys
import getpass

from google.appengine.ext.remote_api import remote_api_stub

import kay.app
from kay.misc import get_appid

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
    
def auth():
  return (raw_input('Username:'), getpass.getpass('Password:'))

def dummy_auth():
  return ('a', 'a')

def create_db_manage_script(main_func=None, clean_func=None, description=None):
  def inner(appid=('a', ''), host=('h', ''), path=('p', ''),
            secure=True, clean=('c', False)):
    if not appid:
      appid = get_appid()
    if not host:
      host = "%s.appspot.com" % appid
    if not path:
      path = '/remote_api'

    if 'localhost' in host:
      auth_func = dummy_auth
    else:
      auth_func = auth

    remote_api_stub.ConfigureRemoteApi(appid, path, auth_func,
                                       host, secure=secure, save_cookies=True)
    remote_api_stub.MaybeInvokeAuthentication()

    if clean and callable(clean_func):
      clean_func()
    if callable(main_func):
      main_func()

  if description:
    inner.__doc__ = description

  return inner
