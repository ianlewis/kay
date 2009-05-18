# -*- coding: utf-8 -*-

import sys
import logging

from werkzeug import Request, ClosingIterator
from werkzeug.exceptions import (
  HTTPException, InternalServerError, NotFound
)
from werkzeug.utils import DispatcherMiddleware

import kay
from kay.utils import local, local_manager
from kay._internal import InternalApp
from kay import utils, exceptions, mail

import settings


def get_application():
  application = KayApp()
  internal_app = InternalApp()
  application = DispatcherMiddleware(application, {
    '/_kay': internal_app,
  })
  return application

class KayApp(object):

  def __init__(self):
    local.application = self
    from urls import make_url, all_views
    self.views = all_views
    self.url_map = make_url()
    self._request_middleware = self._response_middleware = \
        self._view_middleware = self._exception_middleware = None

  def load_middleware(self):
    self._response_middleware = []
    self._view_middleware = []
    self._exception_middleware = []
    request_middleware = []
    from kay.utils.importlib import import_module
    for mw_path in settings.MIDDLEWARE_CLASSES:
      try:
        dot = mw_path.rindex('.')
      except ValueError:
        raise exceptions.ImproperlyConfigured, \
            '%s isn\'t a middleware module' % middleware_path
      mw_module, mw_classname = mw_path[:dot], mw_path[dot+1:]
      try:
        mod = import_module(mw_module)
      except ImportError, e:
        raise exceptions.ImproperlyConfigured, \
            'Error importing middleware %s: "%s"' % (mw_module, e)
      try:
        mw_class = getattr(mod, mw_classname)
      except AttributeError:
        raise exceptions.ImproperlyConfigured, \
            'Middleware module "%s" does not define a "%s" class' % \
            (mw_module, mw_classname)
      try:
        mw_instance = mw_class()
      except exceptions.MiddlewareNotUsed:
        continue

      if hasattr(mw_instance, 'process_request'):
        request_middleware.append(mw_instance.process_request)
      if hasattr(mw_instance, 'process_view'):
        self._view_middleware.append(mw_instance.process_view)
      if hasattr(mw_instance, 'process_response'):
        self._response_middleware.insert(0, mw_instance.process_response)
      if hasattr(mw_instance, 'process_exception'):
        self._exception_middleware.insert(0, mw_instance.process_exception)

    # We only assign to this when initialization is complete as it is used
    # as a flag for initialization being complete.
    self._request_middleware = request_middleware

  def get_response(self, request):
    if self._request_middleware is None:
      self.load_middleware()
    # apply request middleware
    for mw_method in self._request_middleware:
      response = mw_method(request)
      if response:
        return response

    utils.init_jinja2_environ()
    lang = (request.accept_languages.best or 
            settings.DEFAULT_LANG).split('-')[0].lower()
    utils.init_lang(lang)

    try:
      endpoint, values = local.url_adapter.match()
      # TODO: handle view_middleware here if neccesary
      try:
        response = self.views[endpoint](request, **values)
      except Exception, e:
        # If the view raised an exception, run it through exception
        # middleware, and if the exception middleware returns a
        # response, use that. Otherwise, reraise the exception.
        for middleware_method in self._exception_middleware:
          response = middleware_method(request, e)
          if response:
            return response
        raise
    except HTTPException, e:
      logging.warning(e)
      response = e
    except SystemExit:
      # Allow sys.exit() to actually exit.
      raise
    except: # Handle everything else, including SuspiciousOperation, etc.
      # Get the exception info now, in case another exception is thrown later.
      import sys
      exc_info = sys.exc_info()
      return self.handle_uncaught_exception(request, exc_info)
    return response

  def handle_uncaught_exception(self, request, exc_info):
    import os
    if 'SERVER_SOFTWARE' in os.environ and \
          os.environ['SERVER_SOFTWARE'].startswith('Dev'):
      raise
    else:
      subject = 'Error %s: %s' % (request.remote_addr, request.path)
      try:
        from kay.utils import repr
        request_repr = repr.dump(request)
      except Exception, e:
        request_repr = "Request repr() unavailable"
      message = "%s\n\n%s" % (self._get_traceback(exc_info), request_repr)
      mail.mail_admins(subject, message, fail_silently=True)
      # TODO: Return an HttpResponse that displays a friendly error message.
      return InternalServerError()

  def _get_traceback(self, exc_info):
    "Helper function to return the traceback as a string"
    import traceback
    return '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))

  def __call__(self, environ, start_response):
    local.application = self
    local.request = request = Request(environ)
    local.url_adapter = self.url_map.bind_to_environ(environ)

    response = self.get_response(request)

    for middleware_method in self._response_middleware:
      response = middleware_method(request, response)

    return ClosingIterator(response(environ, start_response),
        [local_manager.cleanup])

