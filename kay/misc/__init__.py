# -*- coding: utf-8 -*-

"""
Kay miscellanea.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import os, sys

def get_appid():
  from google.appengine.api import apiproxy_stub_map
  have_appserver = bool(apiproxy_stub_map.apiproxy.GetStub('datastore_v3'))
  if have_appserver:
    appid = os.environ.get('APPLICATION_ID')
  else:
    try:
      from google.appengine.tools import dev_appserver
      from kay import PROJECT_DIR
      appconfig, unused = dev_appserver.LoadAppConfig(PROJECT_DIR, {})
      appid = appconfig.application
    except ImportError:
      appid = None
  return appid

def get_datastore_paths():
  """Returns a tuple with the path to the datastore and history file.

  The datastore is stored in the same location as dev_appserver uses by
  default, but the name is altered to be unique to this project so multiple
  Django projects can be developed on the same machine in parallel.

  Returns:
    (datastore_path, history_path)
  """
  from google.appengine.tools import dev_appserver_main
  datastore_path = dev_appserver_main.DEFAULT_ARGS['datastore_path']
  history_path = dev_appserver_main.DEFAULT_ARGS['history_path']
  datastore_path = datastore_path.replace("dev_appserver", "kay_%s" %
                                          get_appid())
  history_path = history_path.replace("dev_appserver", "kay_%s" %
                                      get_appid())
  return datastore_path, history_path

class NullMemcache(object):
  def get(self, name):
    return None
  def set(self, name, value, ttl):
    return None
