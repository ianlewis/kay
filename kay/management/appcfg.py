# -*- coding: utf-8 -*-

"""
Kay appcfg management command.

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
from kay.utils.importlib import import_module

# TODO: corresponds with SUBMOUNT_APP feature

def find_template_dir(target_path):
  ret = []
  for filename in listdir(target_path):
    target_fullpath = path.join(target_path, filename)
    if path.isdir(target_fullpath):
      if filename.startswith(".") or filename == "kay":
        continue
      if filename == "templates":
        ret.append(target_fullpath)
      else:
        ret = ret + find_template_dir(target_fullpath)
    else:
      continue
  return ret


def compile_app_templates(app):
  app.init_jinja2_environ()
  env = local.jinja2_env
  target_dirs = [dir for dir in app.app_settings.TEMPLATE_DIRS\
                   if os.path.isdir(dir)]
  for app in app.app_settings.INSTALLED_APPS:
    if app.startswith("kay"):
      continue
    mod = import_module(app)
    target_dirs.extend(find_template_dir(os.path.dirname(mod.__file__)))
  for dir in target_dirs:
    dest = dir.replace("templates", "templates_compiled")
    if path.isdir(dest):
      for d, subdirs, files in os.walk(dest):
        for f in files:
          compiled_filename = "%s/%s" % (d, f)
          orig_filename = compiled_filename.replace("templates_compiled",
                                                    "templates")
          if not path.isfile(orig_filename):
            os.unlink(compiled_filename)
            print "%s does not exist. So, '%s' is removed." % (
              orig_filename, compiled_filename)
    else:
      mkdir(dest)
    print "Now compiling templates in %s to %s." % (dir, dest)
    compile_dir(env, dir, dest)


def do_appcfg_passthru_argv():
  from google.appengine.tools import appcfg
  progname = sys.argv[0]
  if len(sys.argv) < 3:
    sys.stderr.write('action required.\n')
    sys.exit(1)
  if sys.argv[2] == 'update':
    print "Compiling templates..."
    app = kay.app.get_application()
    compile_app_templates(app.app) # pass KayApp instance
    for key, submount_app in app.mounts.iteritems():
      if key == "/_kay":
        continue
      compile_app_templates(submount_app)
    print "Finished compiling templates..."
  sys.modules['__main__'] = appcfg
  
  args = sys.argv[2:]
  if "--help" in args:
    args = [progname] + args
  else:
    args = [progname] + args + [os.getcwdu()]
  appcfg.main(args)
  from kay.conf import settings
  if settings.PROFILE and sys.argv[2] == 'update':
    print '--------------------------\n' \
        'WARNING: PROFILER ENABLED!\n' \
        '--------------------------'

def do_appcfg(action='', quiet=('q', False), verbose=('v', False), noisy=False,
              server=('s', 'appengine.google.com'), secure=False,
              email=('e', ''), cookies=True):
  from google.appengine.tools import appcfg
  progname = sys.argv[0]
  args = []
  if not action:
    sys.stderr.write('action required.\n')
    sys.exit(1)
  args.extend([action])
  if quiet:
    args.extend(["--quiet"])
  if verbose:
    args.extend(["--verbose"])
  if noisy:
    args.extend(["--noisy"])
  if server:
    args.extend(["--server", server])
  if secure:
    args.extend(["--secure"])
  if email:
    args.extend(["--email"])
  if not cookies:
    args.extend(["--no_cookies"])
  sys.modules['__main__'] = appcfg
  appcfg.main([progname] + args + [os.getcwdu()])
  from kay.conf import settings
  if settings.PROFILE and action == 'update':
    print '--------------------------\n' \
        'WARNING: PROFILER ENABLED!\n' \
        '--------------------------'

    
