# -*- coding: utf-8 -*-

"""
Kay framework.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     Ian Lewis <IanMLewis@gmail.com>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import os
import sys

import settings

__version__ = "0.7.0"

KAY_DIR = os.path.abspath(os.path.dirname(__file__))
LIB_DIR = os.path.join(KAY_DIR, 'lib')
PROJECT_DIR = os.path.abspath(os.path.dirname(settings.__file__))
PROJECT_LIB_DIR = os.path.join(PROJECT_DIR, 'lib')

def setup_env(manage_py_env=False):
  """Configures app engine environment for command-line apps."""
  # Try to import the appengine code from the system path.
  try:
    from google.appengine.api import apiproxy_stub_map
  except ImportError, e:
    # Not on the system path. Build a list of alternative paths where it
    # may be. First look within the project for a local copy, then look for
    # where the Mac OS SDK installs it.
    paths = [os.path.join(PROJECT_DIR, '.google_appengine'),
             '/usr/local/google_appengine']
    for path in os.environ.get('PATH', '').replace(';', ':').split(':'):
      path = path.rstrip(os.sep)
      if path.endswith('google_appengine'):
        paths.append(path)
    if os.name in ('nt', 'dos'):
      prefix = '%(PROGRAMFILES)s' % os.environ
      paths.append(prefix + r'\Google\google_appengine')
    # Loop through all possible paths and look for the SDK dir.
    SDK_PATH = None
    for sdk_path in paths:
      sdk_path = os.path.realpath(sdk_path)
      if os.path.exists(sdk_path):
        SDK_PATH = sdk_path
        break
    if SDK_PATH is None:
      # The SDK could not be found in any known location.
      sys.stderr.write('The Google App Engine SDK could not be found!\n'
                       'Please visit http://kay-docs.shehas.net/'
                       ' for installation instructions.\n')
      sys.exit(1)
    # Add the SDK and the libraries within it to the system path.
    EXTRA_PATHS = [SDK_PATH]
    lib = os.path.join(SDK_PATH, 'lib')
    # Automatically add all packages in the SDK's lib folder:
    for dir in os.listdir(lib):
      path = os.path.join(lib, dir)
      # Package can be under 'lib/<pkg>/<pkg>/' or 'lib/<pkg>/lib/<pkg>/'
      detect = (os.path.join(path, dir), os.path.join(path, 'lib', dir))
      for path in detect:
        if os.path.isdir(path):
          EXTRA_PATHS.append(os.path.dirname(path))
          break
    sys.path = EXTRA_PATHS + sys.path
    # corresponds with another google package
    if sys.modules.has_key('google'):
      del sys.modules['google']
    from google.appengine.api import apiproxy_stub_map
  setup()

  if not manage_py_env:
    return
  print 'Running on Kay-%s' % __version__

def setup():
  setup_syspath()
  from kay.conf import settings
  from google.appengine.ext import db
  from google.appengine.ext.db import polymodel

  class _meta(object):
    __slots__ = ('object_name', 'app_label', 'module_name', '_db_table', 'abstract')
    def __init__(self, model):
      try:
        self.app_label = model.__module__.split('.')[-2]
      except IndexError:
        raise ValueError('Kay expects models (here: %s.%s) to be defined in their own apps!' % (model.__module__, model.__name__))
      self.module_name = model.__name__.lower()
      self.abstract = model is db.Model
      self.object_name = model.__name__

    def _set_db_table(self, db_table):
      self._db_table = db_table

    def _get_db_table(self):
      if getattr(settings, 'ADD_APP_PREFIX_TO_KIND', True):
        if hasattr(self, '_db_table'):
          return self._db_table
        return '%s_%s' % (self.app_label, self.module_name)
      return self.object_name
    db_table = property(_get_db_table, _set_db_table)

  def _initialize_model(cls):
    cls._meta = _meta(cls)  

  old_propertied_class_init = db.PropertiedClass.__init__
  def __init__(cls, name, bases, attrs, map_kind=True):
    """
    Just add _meta to db.Model.
    """
    _initialize_model(cls)
    old_propertied_class_init(cls, name, bases, attrs,
                              not cls._meta.abstract)
  db.PropertiedClass.__init__ = __init__

  old_poly_init = polymodel.PolymorphicClass.__init__
  def __init__(cls, name, bases, attrs):
    if polymodel.PolyModel not in bases:
      _initialize_model(cls)
    old_poly_init(cls, name, bases, attrs)
  polymodel.PolymorphicClass.__init__ = __init__

  @classmethod
  def kind(cls):
    return cls._meta.db_table
  db.Model.kind = kind


def setup_syspath():
  if not PROJECT_DIR in sys.path:
    sys.path = [PROJECT_DIR] + sys.path
  if not LIB_DIR in sys.path:
    sys.path = [LIB_DIR] + sys.path
  if not PROJECT_LIB_DIR in sys.path:
    sys.path = [PROJECT_LIB_DIR] + sys.path
