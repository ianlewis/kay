#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path
import kay
kay.setup_env(manage_py_env=True)
from werkzeug import script
from kay.misc.script import make_remote_shell
from kay.misc.runserver import start_dev_appserver

def init_remote_shell():
  from google.appengine.ext import db
  def deleteAllEntities(model, num=20):
    entries = db.Query(model, keys_only=True).fetch(num)
    while len(entries) > 0:
      print "Now deleting %d entries." % len(entries)
      db.delete([k.key() for k in entries])
      entries = db.Query(model, keys_only=True).fetch(num)
  return locals()

action_shell = script.make_shell()
action_rshell = make_remote_shell(init_remote_shell)
action_runserver = start_dev_appserver

if __name__ == '__main__':
  script.run()

