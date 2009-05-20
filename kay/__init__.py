# -*- coding: utf-8 -*-
"""
Kay

This is a web framework for GAE/Python.

Requirements:
* WerkZeug
* Jinja2
* pytz
* babel
* simplejson

"""
import os
import sys

__version__ = '0.1'

KAY_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(KAY_DIR)
LIB_DIR = os.path.join(KAY_DIR, 'lib')

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
                       'Visit http://code.google.com/p/app-engine-patch/'
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
    from google.appengine.api import apiproxy_stub_map

  # Add this folder to sys.path
  sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path
  setup()

  if not manage_py_env:
    return
  print 'Running on Kay-%s' % __version__

def setup():
  if not PROJECT_DIR in sys.path:
    sys.path = [PROJECT_DIR] + sys.path
  if not LIB_DIR in sys.path:
    sys.path = [LIB_DIR] + sys.path
