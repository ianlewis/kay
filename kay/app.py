# -*- coding: utf-8 -*-

"""
Kay application.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
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
from werkzeug import (
  Response, redirect
)
from jinja2 import (
  Environment, Undefined,
)
from werkzeug.routing import Submount
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

import kay
from kay.utils import (
  local, local_manager, reverse, render_to_string,
)
from kay.utils.importlib import import_module
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
  elif call == 'Commit':
    from kay.utils.db_hook import execute_reserved_hooks
    execute_reserved_hooks()
  elif call == 'Rollback' or call == 'BeginTransaction':
    from kay.utils.db_hook import clear_reserved_hooks
    clear_reserved_hooks()
    

def get_application(settings=_settings):
  application = KayApp(settings)
  submount_apps = {}
  for app_name in settings.SUBMOUNT_APPS:
    app = KayApp(LazySettings('%s.settings' % app_name))
    submount_apps['/%s' % app_name] = app
  application = DispatcherMiddleware(application, submount_apps)
  return application


class NullUndefined(Undefined):
  """
  Do nothing except for logging when the specified variable doesn't exist.
  """
  __slots__ = ()
  def __int__(self):
    return 0
  def __getattr__(self, value):
    return u''
  def __html__(self):
    self.debug_log()
    return u''
  def debug_log(self):
    f = sys._getframe(1)
    while not 'templates' in f.f_code.co_filename:
      f = f.f_back
    logging.warn("%s: %s is undefined." %
                 (f.f_code.co_filename, self._undefined_name))

def get_app_tailname(app):
  dot = app.rfind('.')
  if dot >= 0:
    return app[dot+1:]
  else:
    return app
  

class KayApp(object):

  def __init__(self, app_settings):
    self.app_settings = app_settings
    self.url_map = None
    self.views = None
    self._request_middleware = self._response_middleware = \
        self._view_middleware = self._exception_middleware = None
    self.auth_backend = None
    self.init_jinja2_environ()

  def get_mount_point(self, app):
    if app == 'kay._internal':
      return '/_kay'
    return self.app_settings.APP_MOUNT_POINTS.get(
      app, "/%s" % get_app_tailname(app))

  def get_installed_apps(self):
    return self.app_settings.INSTALLED_APPS+['kay._internal']

  def init_url_map(self):
    self.has_error_on_init_url_map = False
    mod = import_module(self.app_settings.ROOT_URL_MODULE)

    make_url = getattr(mod, 'make_url')
    all_views = getattr(mod, 'all_views')
    self.views = all_views
    self.url_map = make_url()
    for app in self.get_installed_apps():
      try:
        url_mod = import_module("%s.urls" % app)
      except ImportError:
        logging.warning("Failed to import app '%s.urls', skipped." % app)
        logging.debug("Reason:\n%s" % self._get_traceback(sys.exc_info()))
        continue
      mountpoint = self.get_mount_point(app)
      make_rules = getattr(url_mod, 'make_rules', None)
      if make_rules:
        self.url_map.add(Submount(mountpoint, make_rules()))
      all_views = getattr(url_mod, 'all_views', None)
      if all_views:
        self.views.update(all_views)
    if 'kay.auth.middleware.AuthenticationMiddleware' in \
          self.app_settings.MIDDLEWARE_CLASSES:
      try:
        dot = self.app_settings.AUTH_USER_BACKEND.rindex('.')
      except ValueError:
        raise exceptions.ImproperlyConfigured, \
            'Error importing auth backend %s: "%s"' % \
            (self.app_settings.AUTH_USER_BACKEND, e)
      backend_module, backend_classname = \
          self.app_settings.AUTH_USER_BACKEND[:dot], \
          self.app_settings.AUTH_USER_BACKEND[dot+1:]
      try:
        mod = import_module(backend_module)
      except ImportError, e:
        raise exceptions.ImproperlyConfigured, \
            'Error importing auth backend %s: "%s"' % (backend_module, e)
      try:
        klass = getattr(mod, backend_classname)
      except AttributeError:
        raise exceptions.ImproperlyConfigured, \
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
    per_app_loaders = {}
    for app in self.get_installed_apps():
      try:
        mod = import_module(app)
      except ImportError:
        logging.warning("Failed to import app '%s', skipped." % app)
        continue
      try:
        app_key = getattr(mod, 'template_loader_key')
      except AttributeError:
        app_key = get_app_tailname(app)
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
    self.jinja2_env = Environment(**env_dict)
    for key, filter_str in self.app_settings.JINJA2_FILTERS.iteritems():
      try:
        dot = filter_str.rindex('.')
      except ValueError:
        logging.warn('%s is invalid for JINJA2_FILTERS.' % filter_str)
        continue
      filter_mod, filter_func = filter_str[:dot], filter_str[dot+1:]
      try:
        mod = import_module(filter_mod)
      except ImportError, e:
        logging.warn('Error importing auth backend %s: "%s"' % (filter_mod, e))
        continue
      try:
        func = getattr(mod, filter_func)
      except AttributeError:
        logging.warn('Module "%s" does not define a "%s" func' % 
                     (mod, filter_func))
        continue
      if self.jinja2_env.filters.has_key(key):
        logging.warn('Key "%s" has already defined, skipped.' % key)
        continue
      self.jinja2_env.filters[key] = func

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
      self.jinja2_env.install_gettext_translations(translations)
    else:
      from kay.i18n import KayNullTranslations
      self.active_translations = KayNullTranslations()
      self.jinja2_env.install_null_translations()


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
    if self.app_settings.USE_I18N:
      lang = request.cookies.get(settings.LANG_COOKIE_NAME)
      if not lang:
        lang = (request.accept_languages.best or 
                self.app_settings.DEFAULT_LANG)
      pos = lang.find('-')
      if pos >= 0:
        lang = lang[:pos].lower()+'_'+lang[pos+1:].upper()
      else:
        lang = lang.lower()
    else:
      lang = None
    self.init_lang(lang)
    request.lang = lang

    # apply request middleware
    if self._request_middleware is None:
      self.load_middleware()
    for mw_method in self._request_middleware:
      response = mw_method(request)
      if response:
        return response

    try:
      endpoint, values = local.url_adapter.match()
      view_func = self.views.get(endpoint, None)
      if view_func is None:
        raise NotFound
      if isinstance(view_func, basestring):
        try:
          dot = view_func.rindex('.')
          view_module, view_funcname = view_func[:dot], view_func[dot+1:]
          view_mod = import_module(view_module)
          view_func = getattr(view_mod, view_funcname)
          assert(callable(view_func))
        except StandardError, e:
          logging.error(e)
          raise NotFound
      for mw_method in self._view_middleware:
        response = mw_method(request, view_func, **values)
        if response:
          return response
      try:
        response = view_func(request, **values)
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
    except CapabilityDisabledError, e:
      logging.error(e)
      # Saving session will also fail.
      if hasattr(request, 'session'):
        del(request.session)
      return Response(
        render_to_string(
          "_internal/maintenance.html",
          {"message": _('Appengine might be under maintenance.')}),
        content_type="text/html; charset=utf-8",
        status=503)
    except: # Handle everything else, including SuspiciousOperation, etc.
      # Get the exception info now, in case another exception is thrown later.
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
      logging.error(message)
      if self.app_settings.DEBUG:
        return InternalServerError(message.replace("\n", "<br/>\n"))
      else:
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
    if self.url_map is None or self.has_error_on_init_url_map:
      try:
        self.init_url_map()
      except (StandardError, exceptions.ImproperlyConfigured):
        self.has_error_on_init_url_map = True
        raise
    local.url_adapter = self.url_map.bind_to_environ(environ)

    response = self.get_response(request)

    for middleware_method in self._response_middleware:
      response = middleware_method(request, response)

    return ClosingIterator(response(environ, start_response),
        [local_manager.cleanup])

