# -*- coding: utf-8 -*-

"""
Settings and configuration for Kay.

Values will be read from the module passed when initialization and
then, kay.conf.global_settings; see the global settings file for a
list of all possible variables.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.

Taken from django.
"""

import os
import re
import time     # Needed for Windows

from kay.conf import global_settings
from kay.misc.lazy import LazyObject


class LazySettings(LazyObject):
  """
  A lazy proxy for either global Kay settings or a app local settings
  object. Kay uses the settings module passed to __init__ medthod.
  """
  def __init__(self, settings_module=None):
    super(LazySettings, self).__init__()
    self.settings_module = settings_module or 'settings'

  def __getattr__(self, name):
    if name == 'settigns_module':
      return self.__dict__["settings_module"]
    return super(LazySettings, self).__getattr__(name)

  def __setattr__(self, name, value):
    if name == 'settings_module':
      self.__dict__["settings_module"] = value
    else:
      super(LazySettings, self).__setattr__(name, value)

  def _setup(self):
    """
    Load the settings module passed to the constructor. 
    """
    try:
      if not self.settings_module: # If it's set but is an empty string.
        raise KeyError
    except KeyError:
      # NOTE: This is arguably an EnvironmentError, but that causes
      # problems with Python's interactive help.
      raise ImportError("Settings cannot be imported")

    self._wrapped = Settings(self.settings_module)
    try:
      del self.settings_module
    except AttributeError:
      pass

  def configured(self):
    """
    Returns True if the settings have already been configured.
    """
    return bool(self._wrapped)
  configured = property(configured)


class Settings(object):
  def __init__(self, settings_module):
    from werkzeug.utils import import_string
    # update this dict from global settings (but only for ALL_CAPS settings)
    for setting in dir(global_settings):
      if setting == setting.upper():
        setattr(self, setting, getattr(global_settings, setting))

    # store the settings module in case someone later cares
    self.SETTINGS_MODULE = settings_module

    try:
      mod = import_string(self.SETTINGS_MODULE)
    except ImportError, e:
      raise ImportError, ("Could not import settings '%s' (Is it on sys.path?"
                          " Does it have syntax errors?): %s"
                          % (self.SETTINGS_MODULE, e))

    # Settings that should be converted into tuples if they're
    # mistakenly entered as strings.

    tuple_settings = ("INSTALLED_APPS", "TEMPLATE_DIRS", "SUBMOUNT_APPS")

    for setting in dir(mod):
      if setting == setting.upper():
        setting_value = getattr(mod, setting)
        if setting in tuple_settings and type(setting_value) == str:
          setting_value = (setting_value,) # In case the user forgot the comma.
        setattr(self, setting, setting_value)

    # Expand entries in INSTALLED_APPS like "django.contrib.*" to a list
    # of all those apps.
    new_installed_apps = []
    for app in self.INSTALLED_APPS:
      if app.endswith('.*'):
        app_mod = import_string(app[:-2])
        appdir = os.path.dirname(app_mod.__file__)
        app_subdirs = os.listdir(appdir)
        app_subdirs.sort()
        name_pattern = re.compile(r'[a-zA-Z]\w*')
        for d in app_subdirs:
          if name_pattern.match(d) and os.path.isdir(os.path.join(appdir, d)):
            new_installed_apps.append('%s.%s' % (app[:-2], d))
      else:
        new_installed_apps.append(app)
    self.INSTALLED_APPS = new_installed_apps

  def get_all_members(self):
    return dir(self)

_settings = LazySettings()

class SettingsProxy(object):
  def __getattr__(self, name):
    from kay.utils import local
    try:
      return getattr(local.app.app_settings, name)
    except AttributeError:
      return getattr(_settings, name)

settings = SettingsProxy()
