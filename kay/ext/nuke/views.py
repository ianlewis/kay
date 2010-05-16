# -*- coding: utf-8 -*-

"""
Views of nuke.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp>,
                     Karl Ostmo <kostmo@gmail.com>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import kay
import logging

from werkzeug.utils import import_string
from werkzeug import Response
from google.appengine.ext import db
from google.appengine.api import mail

from kay.utils import (
  render_to_response, render_to_string
)
from kay.cache.decorators import no_cache
from kay.i18n import gettext as _
from kay.conf import settings

def get_all_models():
  ret = []
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
            if c in ret:
              continue
            if issubclass(c, db.polymodel.PolyModel) and \
                  c.__base__ is not db.polymodel.PolyModel:
                continue
            ret.append(c)
        except TypeError:
          pass
  return ret

def get_schema_kinds():
  """Returns the list of kinds for this app."""

  class KindStatError(Exception):
    """Unable to find kind stats for an all-kinds download."""
    pass

  from google.appengine.ext.db import stats
  global_stat = stats.GlobalStat.all().get()
  if not global_stat:
    raise KindStatError()
  timestamp = global_stat.timestamp
  kind_stat = stats.KindStat.all().filter("timestamp =", timestamp).fetch(1000)
  # kind_stat = stats.KindStat.all().fetch(1000) # Experimental
  kind_list = [stat.kind_name for stat in kind_stat
               if stat.kind_name and not stat.kind_name.startswith('__')]
  kind_set = set(kind_list)
  return list(kind_set)

@no_cache
def main_handler(request):
  model_list = get_all_models()
  all_kinds = get_schema_kinds()
  present_kinds = []
  for kind_class in model_list:
    first_entity = kind_class.all(keys_only=True).get()
    if first_entity:
      present_kinds.append(kind_class.kind())
  return render_to_response('nuke/main.html',
                            {'kinds': all_kinds,
                             'present_kinds': present_kinds})

@no_cache
def mass_delete(request):
  import bulkupdate
  model_list = get_all_models()
  kinds = [model.kind() for model in model_list]
  result = None
  nuke_all_kinds = request.form.get('nuke_all_kinds')
  if not nuke_all_kinds:
    kind_string = request.form.get('kind')
    kind_class = None
    for model in model_list:
      if model.kind() == kind_string:
        kind_class = model
    if kind_class:
      job = bulkupdate.BulkDelete(kind_class.all(keys_only=True))
      job.start()
      result = "Deleting all <b>" + kind_string + "</b> entities..."
    else:
      result = "Module does not have the class '%s'." % kind_string
    
  else:
    for kind_class in model_list:
      job = bulkupdate.BulkDelete(kind_class.all(keys_only=True))
      job.start()
    result = "Deleting entities of all kinds!"
  return render_to_response('nuke/result.html',
                            {'result': result})
      
