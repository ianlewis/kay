# -*- coding: utf-8 -*-

"""
kay.handlers

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging

from werkzeug.exceptions import (
  MethodNotAllowed, NotImplemented
)

METHODS = ['GET', 'POST', 'HEAD', 'OPTIONS', 'PUT', 'DELETE', 'TRACE']

class BaseHandler(object):

  def __init__(self):
    pass

  def __call__(self, request, **kwargs):
    self.request = request
    prepare_func = getattr(self, 'prepare', None)
    if callable(prepare_func):
      response = prepare_func()
      if response:
        return response
    if request.method in METHODS:
      func = getattr(self, request.method.lower(), None)
      if callable(func):
        try:
          return func(**kwargs)
        except Exception, e:
          self.handle_exception(e)
          raise
      else:
        return NotImplemented()
    else:
      return MethodNotAllowed()

  def handle_exception(self, exception):
    pass
