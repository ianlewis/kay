# -*- coding: utf-8 -*-

"""
Kay preparse_bundle management command.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import os
import sys
from os import listdir, path, mkdir

import kay
import kay.app
from kay.utils import local
from kay.utils.jinja2utils.compiler import compile_dir

def find_template_dir(target_path):
  ret = []
  for filename in listdir(target_path):
    target_fullpath = path.join(target_path, filename)
    if path.isdir(target_fullpath):
      if filename.startswith(".") or filename == "debug" or \
            filename == "app_template":
        continue
      if filename == "templates":
        ret.append(target_fullpath)
      else:
        ret = ret + find_template_dir(target_fullpath)
    else:
      continue
  return ret

def do_preparse_bundle():
  print "Compiling bundled templates..."
  app = kay.app.get_application()
  app.app.init_jinja2_environ()
  env = local.jinja2_env
  for dir in find_template_dir(kay.KAY_DIR):
    dest = dir.replace("templates", "templates_compiled")
    if not path.isdir(dest):
      mkdir(dest)
    print "Now compiling templates in %s to %s." % (dir, dest)
    compile_dir(env, dir, dest)
  print "Finished compiling bundled templates..."
