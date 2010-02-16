# -*- coding: utf-8 -*-

"""
Kay remote shell management command.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import os
import os.path
import sys
import time
import getpass
import logging
import threading
import Queue
import signal
import atexit

try:
  import readline
  import rlcompleter
except ImportError:
  readline = None

from werkzeug.utils import import_string
from google.appengine.ext import db
from google.appengine.ext.remote_api import remote_api_stub
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub

import kay    
from kay.conf import settings
from kay.utils.repr import dump
from kay.utils.decorators import retry_on_timeout
from kay.misc import get_appid
from kay.misc import get_datastore_paths
from kay.management.utils import print_status

THREAD_NUM = 20
HISTORY_PATH = os.path.expanduser('~/.kay_shell_history')

def get_all_models_as_dict(only_polymodel_base=False):
  ret = {}
  apps = []
  app = kay.app.get_application()
  apps.append(app.app)
  for key, submount_app in app.mounts.iteritems():
    if not hasattr(submount_app, 'app_settings') or key == "/_kay":
      continue
    apps.append(submount_app)
  for kay_app in apps:
    for app in kay_app.app_settings.INSTALLED_APPS:
      try:
        mod = import_string("%s.models" % app)
      except (ImportError, AttributeError), e:
        logging.debug("Failed to import model of an app '%s': '%s', skipped."
                      % (app, e))
        continue
      for name, c in mod.__dict__.iteritems():
        try:
          if issubclass(c, db.Model):
            if c in ret.values():
              continue
            if only_polymodel_base and \
                  issubclass(c, db.polymodel.PolyModel) and \
                  c.__base__ is not db.polymodel.PolyModel:
                continue
            while ret.has_key(name):
              name = name + '_'
            ret[name] = c
        except TypeError:
          pass
  return ret


def auth_func():
  return raw_input('Username:'), getpass.getpass('Password:')


class JobManager(object):
  def __init__(self, models):
    self.queue = Queue.Queue()
    self.finished = dict([[model.kind(), False] for model in models])
    self.counts = dict([[model.kind(), 0] for model in models])
    self.unhandled_counts = dict([[model.kind(), 0] for model in models])

  def add(self, model, job):
    self.queue.put((model, job))
    self.counts[model.kind()] += len(job)

  def set_ready(self, model):
    self.finished[model.kind()] = True

  @property
  def finished_collecting(self):
    for finished in self.finished.values():
      if not finished:
        return False
    return True

  def report_result(self):
    for kind, count in self.counts.iteritems():
      sys.stderr.write("Collected %d of %s.\n" % (count, kind))
    while not self.queue.empty():
      try:
        unused_item = self.queue.get_nowait()
        self.queue.task_done()
        model, job = unused_item
        self.unhandled_counts[model.kind()] += len(job)
      except Queue.Empty:
        pass
    for kind, count in self.unhandled_counts.iteritems():
      if count != 0:
        sys.stderr.write("Unhandled %d of %s.\n" % (count, kind))
      

@retry_on_timeout()
def fetch_from_query(query, size):
  return query.fetch(size)
  

class JobCollector(threading.Thread):
  def __init__(self, job_manager, model, batch_size=20,
               thread_num=THREAD_NUM):
    threading.Thread.__init__(self)
    self.job_manager = job_manager
    self.model = model
    self.batch_size = batch_size
    self.thread_num = thread_num
    self.exit_flag = False
    
  def run(self):
    query = db.Query(self.model, keys_only=True).order("__key__")
    entities = fetch_from_query(query, self.batch_size)
    while entities and not self.exit_flag:
      self.job_manager.add(self.model, entities)
      query = db.Query(self.model, keys_only=True) \
          .order("__key__") \
          .filter("__key__ >", entities[-1])
      entities = fetch_from_query(query, self.batch_size)
    self.job_manager.set_ready(self.model)


@retry_on_timeout()
def delete_entities(entities):
  db.delete(entities)


class DeleteRunner(threading.Thread):

  def __init__(self, job_manager):
    threading.Thread.__init__(self)
    self.job_manager = job_manager
    self.exit_flag = False

  def run(self):
    while not self.exit_flag:
      try:
        (model, entities) = self.job_manager.queue.get_nowait()
        sys.stderr.write("%s is deleting %d of %s entities.\n" %
                         (self.getName(), len(entities), model.kind()))
        sys.stderr.flush()
        delete_entities(entities)
        self.job_manager.queue.task_done()
      except Queue.Empty, e:
        if self.job_manager.finished_collecting:
          return
        else:
          time.sleep(1)


def any_thread_alive(threads):
  for t in threads:
    if t.isAlive():
      return True


def delete_all_entities(models=None, batch_size=20):
  models_dict = get_all_models_as_dict(only_polymodel_base=True)
  if models is None:
    models = models_dict.values()
  if not isinstance(models, list):
    models = [models]
  target_models = []
  for model in models:
    if not (issubclass(model, db.Model) or \
              issubclass(model, db.polymodel.PolyModel)):
      sys.stderr.write("Invalid model: %s\n" % model)
      return
    if model is db.polymodel.PolyModel or model is db.Model:
      continue
    target_models.append(model)
  job_manager = JobManager(target_models)
  threads = []
  for model in target_models:
    job_collector = JobCollector(job_manager, model)
    threads.append(job_collector)
    job_collector.start()
  for i in range(THREAD_NUM):
    t = DeleteRunner(job_manager)
    threads.append(t)
    t.start()
  def handler(signum, frame):
    for t in threads:
      t.exit_flag = True
  signal.signal(signal.SIGINT, handler)
  while any_thread_alive(threads):
    for t in threads:
      if t.isAlive():
        t.join(1)
  job_manager.report_result()


def create_useful_locals():
  local_d = {'db': db,
             'settings': settings,
             'dump': dump}
  local_d.update(get_all_models_as_dict())
  return local_d


def create_useful_locals_for_rshell():
  local_d = {'delete_all_entities': delete_all_entities}
  local_d.update(create_useful_locals())
  return local_d


def shell(datastore_path='', history_path='', useful_imports=True,
          use_ipython=True):
  """ Start a new interactive python session."""
  banner = 'Interactive Kay Shell'
  if useful_imports:
    namespace = create_useful_locals()
  else:
    namespace = {}
  appid = get_appid()
  os.environ['APPLICATION_ID'] = appid
  p = get_datastore_paths()
  if not datastore_path:
    datastore_path = p[0]
  if not history_path:
    history_path = p[1]
  apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
  stub = datastore_file_stub.DatastoreFileStub(appid, datastore_path,
                                               history_path)
  apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)
  if use_ipython:
    try:
      import IPython
    except ImportError:
      pass
    else:
      sh = IPython.Shell.IPShellEmbed(argv='', banner=banner)
      sh(global_ns={}, local_ns=namespace)
      return
  sys.ps1 = '%s> ' % appid
  if readline is not None:
    readline.parse_and_bind('tab: complete')
    atexit.register(lambda: readline.write_history_file(HISTORY_PATH))
    if os.path.exists(HISTORY_PATH):
      readline.read_history_file(HISTORY_PATH)
  from code import interact
  interact(banner, local=namespace)


# TODO: Need refactoring of following three functions.
def create_user(user_name=('u', ''), password=('P', ''), is_admin=('A', False),
                appid=('a', ''), host=('h', ''), path=('p', ''), secure=True):
  """ Create new user using remote_api.
  """
  from kay.auth import (
    create_new_user, DuplicateKeyError,
  )
  if not user_name:
    print_status('user_name required')
    sys.exit(1)
  if not password:
    password = getpass.getpass('Please input a password for new user:')
  if not appid:
    appid = get_appid()
  if not host:
    host = "%s.appspot.com" % appid
  if not path:
    path = '/remote_api'
    
  remote_api_stub.ConfigureRemoteApi(appid, path, auth_func,
                                     host, secure=secure)
  remote_api_stub.MaybeInvokeAuthentication()
  try:
    create_new_user(user_name, password, is_admin=is_admin)
    print_status('A new user: %s successfully created.' % user_name)
    sys.exit(0)
  except DuplicateKeyError, e:
    print_status(e)
    sys.exit(1)


def clear_datastore(appid=('a', ''), host=('h', ''), path=('p', ''),
                    kinds=('k', ''), clear_memcache=('c', False), secure=True):
  """Clear all the data on GAE environment using remote_api.
  """
  if not appid:
    appid = get_appid()
  if not host:
    host = "%s.appspot.com" % appid
  if not path:
    path = '/remote_api'
  if not kinds:
    models = None
  else:
    models_dict = get_all_models_as_dict()
    models = []
    for kind in kinds.split(','):
      models.append(db.class_for_kind(kind))
      
  remote_api_stub.ConfigureRemoteApi(appid, path, auth_func,
                                     host, secure=secure)
  remote_api_stub.MaybeInvokeAuthentication()
  delete_all_entities(models)
  if clear_memcache:
    from google.appengine.api import memcache
    memcache.flush_all()
    sys.stderr.write("Flushed memcache.\n")


def rshell(appid=('a', ''), host=('h', ''), path=('p', ''),
           useful_imports=True, secure=True, use_ipython=True):
  """Start a new interactive python session with RemoteDatastore stub."""
  banner = ("Interactive Kay Shell with RemoteDatastore. \n"
            "-----------------WARNING--------------------\n"
            "\n"
            "Please be careful in this console session.\n"
            "\n"
            "-----------------WARNING--------------------\n")
  if useful_imports:
    namespace = create_useful_locals_for_rshell()
  else:
    namespace = {}
  if not appid:
    appid = get_appid()
  if not host:
    host = "%s.appspot.com" % appid
  if not path:
    path = '/remote_api'

  remote_api_stub.ConfigureRemoteApi(appid, path, auth_func,
                                     host, secure=secure)
  remote_api_stub.MaybeInvokeAuthentication()
  if use_ipython:
    try:
      import IPython
    except ImportError:
      pass
    else:
      sh = IPython.Shell.IPShellEmbed(argv='', banner=banner)
      sh(global_ns={}, local_ns=namespace)
      return
  sys.ps1 = '%s> ' % appid
  if readline is not None:
    readline.parse_and_bind('tab: complete')
    atexit.register(lambda: readline.write_history_file(HISTORY_PATH))
    if os.path.exists(HISTORY_PATH):
      readline.read_history_file(HISTORY_PATH)
  from code import interact
  interact(banner, local=namespace)
