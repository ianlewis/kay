# -*- coding: utf-8 -*-

"""
Kay preparse management command.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import os
import sys
from os import listdir, path, mkdir

from werkzeug.utils import import_string

import kay
import kay.app
from kay.utils import local
from kay.utils.jinja2utils.compiler import compile_dir
from kay.management.utils import print_status

IGNORE_FILENAMES = {
  'kay': ('debug', 'app_template'),
  'app': ('kay'),
}  

def find_template_dir(target_path, ignore_filenames):
  ret = []
  for filename in listdir(target_path):
    target_fullpath = path.join(target_path, filename)
    if path.isdir(target_fullpath):
      if filename.startswith(".") or filename in ignore_filenames:
        continue
      if filename == "templates":
        ret.append(target_fullpath)
      else:
        ret = ret + find_template_dir(target_fullpath, ignore_filenames)
    else:
      continue
  return ret

def do_preparse_bundle():
  """
  Pre compile all the jinja2 templates in Kay itself.
  """
  print_status("Compiling bundled templates...")
  app = kay.app.get_application()
  app.app.init_jinja2_environ()
  env = app.app.jinja2_env
  for dir in find_template_dir(kay.KAY_DIR, ('debug','app_template')):
    dest = prepare_destdir(dir)
    print_status("Now compiling templates in %s to %s." % (dir, dest))
    compile_dir(env, dir, dest)
  print_status("Finished compiling bundled templates...")


def do_preparse_apps():
  """
  Pre compile all the jinja2 templates in your applications.
  """
  from kay.conf import LazySettings
  print_status("Compiling templates...")
  application = kay.app.get_application()
  applications = [application]
  settings_treated = []
  for key, settings_name in \
        application.app.app_settings.PER_DOMAIN_SETTINGS.iteritems():
    if not settings_name in settings_treated:
      applications.append(kay.app.get_application(
          settings=LazySettings(settings_module=settings_name)))
    settings_treated.append(settings_name)
  for app in applications:
    compile_app_templates(app.app) # pass KayApp instance
    for key, submount_app in app.mounts.iteritems():
      if isinstance(submount_app, kay.app.KayApp):
        compile_app_templates(submount_app)

  print_status("Finished compiling templates...")


def prepare_destdir(dir):
  dest = dir.replace("templates", "templates_compiled")
  if path.isdir(dest):
    for d, subdirs, files in os.walk(dest):
      for f in files:
        compiled_filename = "%s/%s" % (d, f)
        orig_filename = compiled_filename.replace("templates_compiled",
                                                  "templates")
        if not path.isfile(orig_filename):
          os.unlink(compiled_filename)
          print_status("%s does not exist. So, '%s' is removed." % (
            orig_filename, compiled_filename))
  else:
    mkdir(dest)
  return dest


def compile_app_templates(app):
  app.init_jinja2_environ()
  env = app.jinja2_env
  target_dirs = [dir for dir in app.app_settings.TEMPLATE_DIRS\
                   if os.path.isdir(dir)]
  for app in app.app_settings.INSTALLED_APPS:
    if app.startswith("kay."):
      continue
    mod = import_string(app)
    target_dirs.extend(find_template_dir(os.path.dirname(mod.__file__),
                                         ('kay')))
  for dir in target_dirs:
    dest = prepare_destdir(dir)
    print_status("Now compiling templates in %s to %s." % (dir, dest))
    compile_dir(env, dir, dest)
