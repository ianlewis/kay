# -*- coding: utf-8 -*-

"""
Kay utilities.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import os
import logging

from werkzeug import (
  Local, LocalManager, Response, Headers
)
from werkzeug.exceptions import NotFound

from kay.conf import settings
from kay.exceptions import ImproperlyConfigured

local = Local()
local_manager = LocalManager([local])

_translations_cache = {}
_default_translations = None
_standard_context_processors = None

_timezone_cache = {}

def set_trace():
  import pdb, sys
  debugger = pdb.Pdb(stdin=sys.__stdin__, 
                     stdout=sys.__stdout__)
  debugger.set_trace(sys._getframe().f_back)

def get_kay_locale_path():
  import kay
  return os.path.join(kay.KAY_DIR, 'i18n')

def _prepare_header():
  if not hasattr(local, "override_headers"):
    local.override_headers = Headers()

def add_header(_key, _value, **_kw):
  _prepare_header()
  local.override_headers.add(_key, _value, **_kw)

def set_header(key, value):
  _prepare_header()
  local.override_headers.set(key, value)

def set_cookie(key, value='', max_age=None, expires=None,
               path='/', domain=None, secure=None, httponly=False):
  if not hasattr(local, "override_cookies"):
    local.override_cookies = []
  local.override_cookies.append({"key": key, "value": value,
                                 "max_age": max_age, "expires": expires,
                                 "path": path, "domain": domain,
                                 "secure": secure, "httponly": httponly})

def delete_cookie(key, path='/', domain=None):
  set_cookie(key, expires=0, max_age=0, path=path, domain=domain)

def get_timezone(tzname):
  """
  Method to get timezone with memcached enhancement.
  """
  global _timezone_cache
  if hasattr(_timezone_cache, 'tzname'):
    tz = _timezone_cache['tzname']
  else:
    from pytz import timezone
    tz = timezone(tzname)
    _timezone_cache['tzname'] = tz
  return tz


def raise_on_dev():
  if 'SERVER_SOFTWARE' in os.environ and \
        os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    raise RuntimeError("Just for debugging.")
  else:
    pass


def get_request():
  return getattr(local, 'request', None)


def url_for(endpoint, **args):
  """Get the URL to an endpoint. There are some special keyword
  arguments:

  `_anchor`
    This string is used as URL anchor.

  `_external`
    If set to `True` the URL will be generated with the full server name
    and `http://` prefix.
  """
  anchor = args.pop('_anchor', None)
  external = args.pop('_external', False)
  rv = local.url_adapter.build(endpoint, args,
                               force_external=external)
  if anchor is not None:
    from werkzeug.urls import url_quote
    rv += '#' + url_quote(anchor)
  return rv

def create_auth_url(url, action):
  if url is None:
    url = local.request.url
  method_name = 'create_%s_url' % action
  if 'kay.auth.middleware.GoogleAuthenticationMiddleware' in \
        settings.MIDDLEWARE_CLASSES:
    from google.appengine.api import users
    method = getattr(users, method_name)
  elif 'kay.auth.middleware.AuthenticationMiddleware' in \
        settings.MIDDLEWARE_CLASSES:
    method = getattr(local.app.auth_backend, method_name)
  return method(url)
      

def create_logout_url(url=None):
  """
  Get the URL for a logout page.
  """
  return create_auth_url(url, 'logout')
    

def create_login_url(url=None):
  """
  Get the URL for a login page.
  """
  return create_auth_url(url, 'login')


def reverse(endpoint, _external=False, method='GET', **values):
  """
  An utility function for jinja2.
  """
  return local.url_adapter.build(endpoint, values, method=method,
      force_external=_external)

def render_error(e):
  from jinja2.exceptions import TemplateNotFound
  from jinja2 import Markup
  try:
    template = local.app.jinja2_env.get_template("%d.html" % e.code)
  except TemplateNotFound:
    template = local.app.jinja2_env.get_template("_internal/defaulterror.html")
  if local.app.jinja2_env.autoescape:
    description = Markup(e.get_description(os.environ))
  else:
    description = e.get_description(os.environ)
  context = {"code": e.code, "name": e.name, "description": description}
  processors = ()
  for processor in get_standard_processors() + processors:
    context.update(processor(get_request()))
  return Response(template.render(context),
                  content_type="text/html; charset=utf-8",
                  status=e.code)

def render_to_string(template, context={}, processors=None):
  """
  A function for template rendering adding useful variables to context
  automatically, according to the CONTEXT_PROCESSORS settings.
  """
  if processors is None:
    processors = ()
  else:
    processors = tuple(processors)
  for processor in get_standard_processors() + processors:
    context.update(processor(get_request()))
  template = local.app.jinja2_env.get_template(template)
  return template.render(context)


def render_to_response(template, context={}, mimetype='text/html',
                       processors=None):
  """
  A function for render html pages.
  """
  return Response(render_to_string(template, context, processors),
                  mimetype=mimetype)

def get_standard_processors():
  from werkzeug.utils import import_string
  from kay.conf import settings
  global _standard_context_processors
  if _standard_context_processors is None:
    processors = []
    for path in settings.CONTEXT_PROCESSORS:
      try:
        func = import_string(path)
      except (ImportError, AttributeError), e:
        raise ImproperlyConfigured('Error importing request processor module'
                                   ' %s: "%s"' % (path, e))
      processors.append(func)
    _standard_context_processors = tuple(processors)
  return _standard_context_processors


def to_local_timezone(datetime, tzname=settings.DEFAULT_TIMEZONE):
  """Convert a datetime object to the local timezone."""
  if datetime.tzinfo is None:
    from pytz import UTC
    datetime = datetime.replace(tzinfo=UTC)
  tzinfo = get_timezone(tzname)
  return tzinfo.normalize(datetime.astimezone(tzinfo))


def to_utc(datetime, tzname=settings.DEFAULT_TIMEZONE):
  """Convert a datetime object to UTC and drop tzinfo."""
  from pytz import UTC
  if datetime.tzinfo is None:
    datetime = get_timezone(tzname).localize(datetime)
  return datetime.astimezone(UTC).replace(tzinfo=None)


def get_by_key_name_or_404(model_class, key_name):
  obj = model_class.get_by_key_name(key_name)
  if not obj:
    raise NotFound
  return obj


def get_by_id_or_404(model_class, id):
  obj = model_class.get_by_id(id)
  if not obj:
    raise NotFound
  return obj


def get_or_404(model_class, key):
  obj = model_class.get(key)
  if not obj:
    raise NotFound
  return obj
