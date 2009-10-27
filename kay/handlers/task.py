# -*- coding: utf-8 -*-

"""
kay.handlers.task

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging

from google.appengine.ext.deferred import (
  run, PermanentTaskFailure
)
from werkzeug import Response

from kay.handlers import BaseHandler

class TaskHandler(BaseHandler):
  def __init__(self):
    import kay.sessions
    import kay.cache
    super(TaskHandler, self).__init__()
    setattr(self, kay.sessions.NO_SESSION, True)
    setattr(self, kay.cache.NO_CACHE, True)

  def post(self):
    headers = ["%s:%s" % (k, v) for k, v in self.request.headers.items()
               if k.lower().startswith("x-appengine-")]
    logging.info(", ".join(headers))
    try:
      run(self.request.data)
    except PermanentTaskFailure, e:
      logging.exception("Permanent failure attempting to execute task: %s." %
                        e)
    return Response("OK")

task_handler = TaskHandler()
