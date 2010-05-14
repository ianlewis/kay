# -*- coding: utf-8 -*-

"""
Kay bulkload management command.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import os
import os.path
import sys
import datetime
import logging
import copy
import getpass
from os import makedirs

from google.appengine.tools import bulkloader

import kay
from kay.misc import get_appid
from kay.management.utils import print_status
from shell import get_all_models_as_dict

DUMP = 1
RESTORE = 2

def do_bulkloader_passthru_argv():
  """
  Execute bulkloader script with appropriate parameters. For more
  details, please invoke 'python manage.py bulkloader --help'.
  """
  progname = sys.argv[0]
  models = get_all_models_as_dict()
  args = []
  for arg in sys.argv[1:]:
    args.append(arg)
  if '--help' in args:
    print_status(bulkloader.__doc__ % {'arg0': "manage.py bulkloader"})
    sys.stdout.flush()
    sys.stderr.flush()
    sys.exit(0)
    
  sys.exit(bulkloader.main(args))

do_bulkloader_passthru_argv.passthru = True


cached_email = None
cached_password = None

def dummy_auth_func(self, raw_input_fn=None, password_input_fn=None):
  self.auth_called = True
  return ("admin", "pass")

def real_auth_func(self, 
                   raw_input_fn=raw_input,
                   password_input_fn=getpass.getpass):
  global cached_email, cached_password
  if self.email:
    email = self.email
  else:
    if cached_email is None:
      print 'Please enter login credentials for %s' % (self.host)
      email = raw_input_fn('Email: ')
      cached_email = email
    else:
      email = cached_email

  if email:
    password_prompt = 'Password for %s: ' % email
    if cached_password is None:
      if self.passin:
        password = raw_input_fn(password_prompt)
      else:
        password = password_input_fn(password_prompt)
      cached_password = password
    else:
      password = cached_password
  else:
    password = None

  self.auth_called = True
  return (email, password)
  

def dump_or_restore_all(help, data_set_name, app_id, url, directory, op):
  if help:
    print_status('help for %s' % op)
    sys.exit(0)
  if not data_set_name:
    data_set_name = datetime.datetime.now().strftime("%Y%m%d.%H%M%S")
  if not app_id:
    app_id = get_appid()
  if not url:
    url = "https://%s.appspot.com/remote_api" % app_id
  if not directory:
    directory = '_backup'
  target_dir = os.path.join(kay.PROJECT_DIR, directory, data_set_name)

  if not os.path.isdir(target_dir):
    if op == DUMP:
      makedirs(target_dir)
      print_status('Directory "%s" created.' % target_dir)
    else:
      print_status('Directory "%s" is missing, exiting...' % target_dir)
      sys.exit(1)
      
  current_time = datetime.datetime.now().strftime("%Y%m%d.%H%M%S")
  models = get_all_models_as_dict(only_polymodel_base=True)
  results = {}
  if op == RESTORE:
    base_args = ["bulkloader", "--restore"]
  else:
    base_args = ["bulkloader", "--dump"]
  if "localhost" in url:
    base_args.append("--app_id=%s" % app_id)
    bulkloader.RequestManager.AuthFunction = dummy_auth_func
  else:
    bulkloader.RequestManager.AuthFunction = real_auth_func
  for key, model in models.iteritems():
    kind = model.kind()
    db_filename = os.path.join(target_dir, "bulkloader-%s-%s.progress" %
                               (kind, current_time))
    log_file = os.path.join(target_dir, "bulkloader-%s-%s.log" %
                            (kind, current_time))
    result_db_filename = os.path.join(target_dir, "bulkloader-%s-%s.result" %
                                      (kind, current_time))
    args = copy.copy(base_args)
    args.append("--filename=%s" % os.path.join(target_dir, "%s.dat" % kind))
    args.append("--kind=%s" % kind)
    args.append("--db_filename=%s" % db_filename)
    args.append("--log_file=%s" % log_file)
    if op == DUMP:
      args.append("--result_db_filename=%s" % result_db_filename)
    args.append("--url=%s" % url)
    try:
      from werkzeug.utils import import_string
      backup_mod = import_string(directory)
      if op == RESTORE:
        args.extend(backup_mod.restore_options[kind])
      else:
        args.extend(backup_mod.dump_options[kind])
    except:
      pass
    try:
      results[key] = bulkloader.main(args)
    except bulkloader.FileNotFoundError, e:
      print_status("File not found, skipped: %s" % e)
      results[key] = -1
      continue
    logging.getLogger('google.appengine.tools.bulkloader').handlers = []
  sys.exit(0)


def dump_all(help=False, data_set_name=('n', ''), app_id=('i', ''),
             url=('u', ''), directory=('d', '')):
  dump_or_restore_all(help, data_set_name, app_id, url, directory, DUMP)

def restore_all(help=False, data_set_name=('n', ''), app_id=('i', ''),
                url=('u', ''), directory=('d', '')):
  dump_or_restore_all(help, data_set_name, app_id, url, directory, RESTORE)
