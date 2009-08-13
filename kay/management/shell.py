# -*- coding: utf-8 -*-

"""
Kay remote shell management command.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import os
import sys
import getpass
import logging

from google.appengine.ext import db
from google.appengine.ext.remote_api import remote_api_stub
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub
    
from kay.conf import settings
from kay.utils.importlib import import_module
from kay.utils.repr import dump
from kay.misc import get_appid
from kay.misc import get_datastore_paths

def get_all_models_as_dict():
  ret = {}
  for app in settings.INSTALLED_APPS:
    try:
      mod = import_module("%s.models" % app)
    except ImportError:
      logging.warning("Failed to import app '%s', skipped.")
      continue
    for name, c in mod.__dict__.iteritems():
      try:
        if issubclass(c, db.Model):
          while ret.has_key(name):
            name = name + '_'
          ret[name] = c
      except TypeError:
        pass
  return ret


def auth_func():
  return raw_input('Username:'), getpass.getpass('Password:')


def delete_all_entities(model, num=20):
  entries = db.Query(model, keys_only=True).fetch(num)
  while len(entries) > 0:
    print "Now deleting %d entries." % len(entries)
    db.delete([k.key() for k in entries])
    entries = db.Query(model, keys_only=True).fetch(num)


def create_useful_locals():
  local_d = {'db': db,
             'settings': settings,
             'dump': dump}
  local_d.update(get_all_models_as_dict())
  return local_d


def create_useful_locals_for_rshell():
  local_d = {'delete_all_entities': delete_all_entities}
  local_d.update(create_useful_locals())
  return local_d


def shell(datastore_path='', history_path='', useful_imports=True):
  """ Start a new interactive python session."""
  banner = 'Interactive Kay Shell'
  if useful_imports:
    namespace = create_useful_locals()
  else:
    namespace = {}
  appid = get_appid()
  os.environ['APPLICATION_ID'] = appid
  p = get_datastore_paths()
  if not datastore_path:
    datastore_path = p[0]
  if not history_path:
    history_path = p[1]
  apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
  stub = datastore_file_stub.DatastoreFileStub(appid, datastore_path,
                                               history_path)
  apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)

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

def rshell(appid=('a', ''), host=('h', ''), path=('p', ''),
           useful_imports=True, secure=True):
  """Start a new interactive python session with RemoteDatastore stub."""
  banner = ("Interactive Kay Shell with RemoteDatastore. \n"
            "-----------------WARNING--------------------\n"
            "\n"
            "Please be careful in this console session.\n"
            "\n"
            "-----------------WARNING--------------------\n")
  if useful_imports:
    namespace = create_useful_locals_for_rshell()
  else:
    namespace = {}
  if not appid:
    appid = get_appid()
  if not host:
    host = "%s.appspot.com" % appid
  if not path:
    path = '/remote_api'

  remote_api_stub.ConfigureRemoteApi(appid, path, auth_func,
                                     host, secure=secure)
  remote_api_stub.MaybeInvokeAuthentication()

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
