# -*- coding: utf-8 -*-

"""
An extended CGIHandler corresponds with a buggy behaviour with
os.environ.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from wsgiref.handlers import CGIHandler

class KayHandler(CGIHandler):
  """
  wsgiref.handlers.CGIHandler holds os.environ when imported.
  This class override this behaviour.
  """
  def __init__(self):
    self.os_environ = {}
    CGIHandler.__init__(self)
