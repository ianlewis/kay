# -*- coding: utf-8 -*-

from wsgiref.handlers import CGIHandler

class KayHandler(CGIHandler):
  """
  wsgiref.handlers.CGIHandler holds os.environ when imported.
  This class override this behaviour.
  """
  def __init__(self):
    self.os_environ = {}
    CGIHandler.__init__(self)
