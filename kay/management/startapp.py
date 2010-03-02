# -*- coding: utf-8 -*-

"""
Kay startapp management commands.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import os
import sys
import re
import shutil

import kay
from kay.management.utils import print_status

def startproject(proj_name=''):
  """
  Start new application.
  """
  if not proj_name:
    sys.stderr.write("proj_name required.\n")
    sys.exit(1)
  directory = os.getcwd()
  if not re.search(r'^[a-zA-Z][a-zA-Z0-9\-]*$', proj_name):
    # If it's not a valid directory name.
    # Provide a smart error message, depending on the error.
    if not re.search(r'^[a-zA-Z]', proj_name):
      message = 'make sure the name begins with a letter'
    else:
      message = 'use only numbers, letters and dashes'
    sys.stderr.write("%r is not a valid project name. Please %s.\n" %
                     (proj_name, message))
    sys.exit(1)
  top_dir = os.path.join(directory, proj_name)
  try:
    os.mkdir(top_dir)
  except OSError, e:
    sys.stderr.write("Failed to mkdir: %s\n" % e)
    sys.exit(1)
  link_paths = ['kay', 'manage.py']
  copy_paths = ['settings.py', 'urls.py', 'favicon.ico']
  for path in link_paths:
    src = os.path.join(kay.PROJECT_DIR, path)
    dest = os.path.join(top_dir, path)
    try:
      os.symlink(src, dest)
    except:
      try:
        shutil.copytree(src, dest)
      except:
        shutil.copyfile(src, dest)
  for path in copy_paths:
    src = os.path.join(kay.PROJECT_DIR, path)
    dest = os.path.join(top_dir, path)
    shutil.copyfile(src, dest)
  path_old = os.path.join(kay.PROJECT_DIR, 'app.yaml')
  path_new = os.path.join(top_dir, 'app.yaml')
  fp_old = open(path_old, 'r')
  fp_new = open(path_new, 'w')
  fp_new.write(fp_old.read().replace('%PROJ_NAME%', proj_name))
  fp_old.close()
  fp_new.close()
  try:
    shutil.copymode(path_old, path_new)
    _make_writeable(path_new)
  except OSError:
    sys.stderr.write(style.NOTICE("Notice: Couldn't set permission bits "
                                  "on %s. You're probably using an "
                                  "uncommon filesystem setup. No "
                                  "problem.\n" % path_new))
  print_status("Finished creating new project: %s." % proj_name)
  
  

def startapp(app_name=''):
  """
  Start new application.
  """
  if not app_name:
    sys.stderr.write("app_name required.\n")
    sys.exit(1)
  try:
    __import__(app_name)
  except ImportError:
    pass
  else:
    sys.stderr.write("%r conflicts with the name of an existing Python"
                     " module and cannot be used as an app name."
                     " Please try another name.\n" % app_name)
    sys.exit(1)
  directory = os.getcwd()
  if not re.search(r'^[_a-zA-Z]\w*$', app_name): # If it's not a valid directory name.
    # Provide a smart error message, depending on the error.
    if not re.search(r'^[_a-zA-Z]', app_name):
      message = 'make sure the name begins with a letter or underscore'
    else:
      message = 'use only numbers, letters and underscores'
    sys.stderr.write("%r is not a valid app name. Please %s.\n" % (app_name, message))
    sys.exit(1)
  top_dir = os.path.join(directory, app_name)
  try:
    os.mkdir(top_dir)
  except OSError, e:
    sys.stderr.write("Failed to mkdir: %s\n" % e)
    sys.exit(1)

  # Determine where the app or project templates are.
  template_dir = os.path.join(os.path.dirname(__file__), 'app_template')

  for d, subdirs, files in os.walk(template_dir):
    relative_dir = d[len(template_dir)+1:].replace('app_name', app_name)
    if relative_dir:
      os.mkdir(os.path.join(top_dir, relative_dir))
    for i, subdir in enumerate(subdirs):
      if subdir.startswith('.'):
        del subdirs[i]
    for f in files:
      if f.endswith('.pyc') or f.endswith('.py~'):
        continue
      path_old = os.path.join(d, f)
      path_new = os.path.join(top_dir, relative_dir, f.replace('app_name',
                                                               app_name))
      fp_old = open(path_old, 'r')
      fp_new = open(path_new, 'w')
      fp_new.write(fp_old.read().replace('%app_name%', app_name))
      fp_old.close()
      fp_new.close()
      try:
        shutil.copymode(path_old, path_new)
        _make_writeable(path_new)
      except OSError:
        sys.stderr.write(style.NOTICE("Notice: Couldn't set permission bits "
                                      "on %s. You're probably using an "
                                      "uncommon filesystem setup. No "
                                      "problem.\n" % path_new))

def _make_writeable(filename):
  """
  Make sure that the file is writeable. Useful if our source is
  read-only.
   
  """
  import stat
  if sys.platform.startswith('java'):
    # On Jython there is no os.access()
    return
  if not os.access(filename, os.W_OK):
    st = os.stat(filename)
    new_permissions = stat.S_IMODE(st.st_mode) | stat.S_IWUSR
    os.chmod(filename, new_permissions)
