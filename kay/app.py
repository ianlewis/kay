# -*- coding: utf-8 -*-

"""
Kay application.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import sys
import os
import logging

from werkzeug import (
  Request, ClosingIterator, DispatcherMiddleware,
)
from werkzeug.exceptions import (
  HTTPException, InternalServerError, NotFound
)
from werkzeug import Response
from jinja2 import (
  Environment, Undefined,
)
from werkzeug.routing import Submount

import kay
from kay.utils import local, local_manager
from kay.utils.importlib import import_module
from kay._internal import InternalApp
from kay import (
  utils, exceptions, mail,
)
from kay.utils.filters import nl2br

from kay.conf import settings, _settings, LazySettings

translations_cache = {}

def model_name_from_key(key):
  return key.path().element_list()[0].type()
    
def db_hook(service, call, request, response):
  if call == 'Put':
    from kay.utils.db_hook import execute_hooks
    for key, entity in zip(response.key_list(), request.entity_list()):
      kind = model_name_from_key(key)
      execute_hooks(kind, key, entity)

def get_application():
  application = KayApp(_settings)
  internal_app = InternalApp()
  submount_apps = {'/_kay': internal_app}
  for app_name in _settings.SUBMOUNT_APPS:
    app = KayApp(LazySettings('%s.settings' % app_name))
    submount_apps['/%s' % app_name] = app
  application = DispatcherMiddleware(application, submount_apps)
  return application

class NullUndefined(Undefined):
  """
  Do nothing except for logging when the specified variable doesn't exist.
  """
  def __int__(self):
    return 0
  def __getattr__(self, value):
    logging.debug("The variable '%s' undefined." % self._undefined_name)
    return u''
  def __html__(self):
    logging.debug("The variable '%s' undefined." % self._undefined_name)
    return u''


class KayApp(object):

  def __init__(self, app_settings):
    self.app_settings = app_settings
    self.url_map = None
    self.views = None
    self._request_middleware = self._response_middleware = \
        self._view_middleware = self._exception_middleware = None
    self.auth_backend = None

  def init_url_map(self):

    mod = import_module(self.app_settings.ROOT_URL_MODULE)

    make_url = getattr(mod, 'make_url')
    all_views = getattr(mod, 'all_views')
    self.views = all_views
    self.url_map = make_url()
    for app in self.app_settings.INSTALLED_APPS:
      try:
        url_mod = import_module("%s.urls" % app)
      except ImportError:
        logging.warning("Failed to import app '%s.urls', skipped." % app)
        continue
      mountpoint = self.app_settings.APP_MOUNT_POINTS.get(app, "/%s" % app)
      make_rules = getattr(url_mod, 'make_rules', None)
      if make_rules:
        self.url_map.add(Submount(mountpoint, make_rules()))
      all_views = getattr(url_mod, 'all_views', None)
      if all_views:
        self.views.update(all_views)
    if 'kay.auth.middleware.AuthenticationMiddleware' in \
          settings.MIDDLEWARE_CLASSES:
      try:
        dot = settings.AUTH_USER_BACKEND.rindex('.')
      except ValueError:
        raise exceptions.ImproperlyConfigured, \
            'Error importing auth backend %s: "%s"' % \
            (settings.AUTH_USER_BACKEND, e)
      backend_module, backend_classname = settings.AUTH_USER_BACKEND[:dot], \
          settings.AUTH_USER_BACKEND[dot+1:]
      try:
        mod = import_module(backend_module)
      except ImportError, e:
        raise ImproperlyConfigured, \
            'Error importing auth backend %s: "%s"' % (backend_module, e)
      try:
        klass = getattr(mod, backend_classname)
      except AttributeError:
        raise ImproperlyConfigured, \
            'Auth backend module "%s" does not define a "%s" class' % \
            (backend_module, backend_classname)
      self.auth_backend = klass()
    
  def init_jinja2_environ(self):
    """
    Initialize the environment for jinja2.
    TODO: Capability to disable i18n stuff.
    TODO: Pluggable utility mechanism.
    """
    if 'SERVER_SOFTWARE' in os.environ and \
          os.environ['SERVER_SOFTWARE'].startswith('Dev'):
      from jinja2 import (FileSystemLoader, ChoiceLoader, PrefixLoader,)
      template_dirname = "templates"
    else:
      from kay.utils.jinja2utils.code_loaders import FileSystemCodeLoader as \
          FileSystemLoader
      from kay.utils.jinja2utils.code_loaders import ChoiceCodeLoader as \
          ChoiceLoader
      from kay.utils.jinja2utils.code_loaders import PrefixCodeLoader as \
          PrefixLoader
      template_dirname = "templates_compiled"
    global local
    per_app_loaders = {}
    for app in self.app_settings.INSTALLED_APPS:
      try:
        mod = import_module(app)
      except ImportError:
        logging.warning("Failed to import app '%s', skipped." % app)
        continue
      try:
        app_key = getattr(mod, 'template_loader_key')
      except AttributeError:
        app_key = app
      per_app_loaders[app_key] = FileSystemLoader(
        os.path.join(os.path.dirname(mod.__file__), template_dirname))
    loader = PrefixLoader(per_app_loaders)  
    if self.app_settings.TEMPLATE_DIRS:
      target = [d.replace("templates", template_dirname)
                for d in self.app_settings.TEMPLATE_DIRS]
      import kay
      base_loader = FileSystemLoader(
        [os.path.join(kay.PROJECT_DIR, d) for d in target])
      loader = ChoiceLoader([base_loader, loader])
    env_dict = dict(
      loader = loader,
      autoescape=True,
      undefined=NullUndefined,
      extensions=['jinja2.ext.i18n'],
    )
    jinja2_env = Environment(**env_dict)
    jinja2_env.filters['nl2br'] = nl2br
    local.jinja2_env = jinja2_env

  def init_lang(self, lang):
    """
    Initialize translations with specified language.
    """
    from kay.i18n import load_translations
    global translations_cache
    if self.app_settings.USE_I18N:
      translations = translations_cache.get("%s:%s" %
                                            (self.app_settings.APP_NAME, lang),
                                            None)
      if translations is None:
        translations = load_translations(lang)
        translations_cache["trans:%s:%s" %
                     (self.app_settings.APP_NAME, lang)] = translations
      self.active_translations = translations
      local.jinja2_env.install_gettext_translations(translations)
    else:
      from kay.i18n import KayNullTranslations
      self.active_translations = NullTranslations()
      local.jinja2_env.install_null_translations()


  def load_middleware(self):
    self._response_middleware = []
    self._view_middleware = []
    self._exception_middleware = []
    request_middleware = []
    for mw_path in self.app_settings.MIDDLEWARE_CLASSES:
      try:
        dot = mw_path.rindex('.')
      except ValueError:
        raise exceptions.ImproperlyConfigured, \
            '%s isn\'t a middleware module' % mw_path
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

    self.init_jinja2_environ()
    lang = (request.accept_languages.best or 
            self.app_settings.DEFAULT_LANG)
    pos = lang.find('-')
    if pos >= 0:
      lang = lang[:pos].lower()+'_'+lang[pos+1:].upper()
    else:
      lang = lang.lower()
    self.init_lang(lang)

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
    kay.setup_syspath()
    if _settings.USE_DB_HOOK:
      from google.appengine.api import apiproxy_stub_map
      apiproxy_stub_map.apiproxy.GetPostCallHooks().Clear()
      apiproxy_stub_map.apiproxy.GetPostCallHooks().Append(
        'db_hook', db_hook, 'datastore_v3')
    local.app = self
    local.request = request = Request(environ)
    if self.url_map is None:
      self.init_url_map()
    local.url_adapter = self.url_map.bind_to_environ(environ)

    response = self.get_response(request)

    for middleware_method in self._response_middleware:
      response = middleware_method(request, response)

    return ClosingIterator(response(environ, start_response),
        [local_manager.cleanup])

