# -*- coding: utf-8 -*-

"""
Kay remote shell management command.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import logging

def init_remote_shell():
  from google.appengine.ext import db
  from kay.conf import settings
  from kay.utils.importlib import import_module
  def deleteAllEntities(model, num=20):
    entries = db.Query(model, keys_only=True).fetch(num)
    while len(entries) > 0:
      print "Now deleting %d entries." % len(entries)
      db.delete([k.key() for k in entries])
      entries = db.Query(model, keys_only=True).fetch(num)
  local_d = locals()
  for app in settings.INSTALLED_APPS:
    try:
      mod = import_module("%s.models" % app)
    except ImportError:
      logging.warning("Failed to import app '%s', skipped.")
      continue
    for name, c in mod.__dict__.iteritems():
      try:
        if issubclass(c, db.Model):
          local_d[name] = c
      except TypeError:
        pass
  return local_d

def make_remote_shell(init_func=None, banner=None, use_ipython=True):
  if banner is None:
    banner = 'Interactive Kay Remote Shell'
  if init_func is None:
    init_func = dict
  def action(appid=('a', ''), host=('h', ''), ipython=use_ipython):
    """Start a new interactive python session."""
    import sys
    import getpass
    from google.appengine.ext.remote_api import remote_api_stub
    from kay.misc import get_appid
    namespace = init_func()
    def auth_func():
      return raw_input('Username:'), getpass.getpass('Password:')
    if not appid:
      appid = get_appid()
    if not host:
      host = "%s.appspot.com" % appid
    remote_api_stub.ConfigureRemoteDatastore(appid, '/remote_api', auth_func,
                                             host)
    if ipython:
      try:
        import IPython
      except ImportError:
        pass
      else:
        sh = IPython.Shell.IPShellEmbed(argv='', banner=banner)
        sh(global_ns={}, local_ns=namespace)
        return
    from code import interact
    interact(banner, local=namespace)
  return action
