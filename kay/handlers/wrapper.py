"""
kay.handlers.wrapper
"""

from werkzeug import Response

class WsgiApplicationHandler(object):
  def __init__(self, app):
    self.__name__ = self.__class__.__name__
    self.app = app

  def __call__(self, request, **kwargs):
    self.request = request
    response = Response.from_app(self.app, self.request.environ)
    return response
