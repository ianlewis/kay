# -*- coding: utf-8 -*-

import os
import logging
from datetime import datetime

from google.appengine.api import users
from google.appengine.api import memcache

from werkzeug import (
  Local, LocalManager, Response
)
from werkzeug.exceptions import NotFound
from jinja2 import (
  Environment, FileSystemLoader, ChoiceLoader, PrefixLoader,
  Undefined,
)
from pytz import timezone, UTC

from kay.conf import settings

local = Local()
local_manager = LocalManager([local])

_translations_cache = {}
_default_translations = None


def get_project_path():
  return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def get_kay_locale_path():
  return os.path.join(get_project_path(), 'kay', 'i18n')


def get_timezone(tzname):
  """
  Method to get timezone with memcached enhancement.
  """
  try:
    tz = memcache.get("tz:%s" % tzname)
  except:
    tz = None
    logging.debug("timezone get failed: %s" % tzname)
  if tz is None:
    tz = timezone(tzname)
    memcache.add("tz:%s" % tzname, tz, 86400)
    logging.debug("timezone memcache added: %s" % tzname)
  else:
    logging.debug("timezone memcache hit: %s" % tzname)

  return tz


def raise_on_dev():
  if 'SERVER_SOFTWARE' in os.environ and \
        os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    raise RuntimeError("Just for debugging.")
  else:
    pass


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


def get_request():
  return local.request


def url_for(endpoint, **args):
  """Get the URL to an endpoint.  The keyword arguments provided are used
  as URL values.  Unknown URL values are used as keyword argument.
  Additionally there are some special keyword arguments:

  `_anchor`
    This string is used as URL anchor.

  `_external`
    If set to `True` the URL will be generated with the full server name
    and `http://` prefix.
  """
  if hasattr(endpoint, 'get_url_values'):
    rv = endpoint.get_url_values()
    if rv is not None:
      if isinstance(rv, basestring):
        return make_external_url(rv)
      endpoint, updated_args = rv
      args.update(updated_args)
  anchor = args.pop('_anchor', None)
  external = args.pop('_external', False)
  rv = local.url_adapter.build(endpoint, args,
                               force_external=external)
  if anchor is not None:
    rv += '#' + url_quote(anchor)
  return rv


def init_lang(lang):
  """
  Initialize translations with specified language.
  """
  global local, _translations_cache
  from kay.i18n import load_translations
  jinja2_env = getattr(local, 'jinja2_env', None)

  if use_i18n():
    try:
      translations = _translations_cache[lang]
    except KeyError:
      translations = load_translations(lang)
    _translations_cache[lang] = translations
    setattr(local, 'active_translations', translations)
    jinja2_env.install_gettext_translations(translations)
  else:
    from gettext import NullTranslations
    setattr(local, 'active_translations', NullTranslations())
    jinja2_env.install_null_translations()


def use_i18n():
  return settings.USE_I18N


def use_session():
  return 'kay.middleware.session.SessionMiddleware' in \
      settings.MIDDLEWARE_CLASSES


def init_jinja2_environ():
  """
  Initialize the environment for jinja2.
  TODO: Capability to disable i18n stuff.
  TODO: Pluggable utility mechanism.
  """
  global local
  base_loader = FileSystemLoader(settings.TEMPLATE_DIRS)
  per_app_loaders = {}
  for app in settings.INSTALLED_APPS:
    per_app_loaders[app] = FileSystemLoader(os.path.join(app, 'templates'))

  env_dict = dict(
    loader = ChoiceLoader([
      base_loader,
      PrefixLoader(per_app_loaders),
    ]),
    autoescape=True,
    undefined=NullUndefined,
    extensions=['jinja2.ext.i18n'],
  )
  
  jinja2_env = Environment(**env_dict)
  jinja2_env.globals.update({'url_for': url_for,
                             'reverse': reverse,
                             'request': local.request,
                             'create_login_url': create_login_url,
                             'create_logout_url': create_logout_url})

  setattr(local, 'jinja2_env', jinja2_env)


def get_active_translations():
  """
  Return active translations tied with the local env.
  """
  global _default_translations
  ret = getattr(local, 'active_translations', None)
  if ret is not None:
    return ret

  if _default_translations is None:
    from kay.i18n import load_translations
    _default_translations = load_translations(settings.DEFAULT_LANG)
  return _default_translations


def create_logout_url(request=None):
  """
  An utilyty function for jinja2.
  """
  # TODO: Change implementation according to auth backend settings.
  from google.appengine.api import users
  if request is None:
    request = local.request
  return users.create_logout_url(request.url)


def create_login_url(request=None):
  """
  An utilyty function for jinja2.
  """
  # TODO: Change implementation according to auth backend settings.
  from google.appengine.api import users
  if request is None:
    request = local.request
  return users.create_login_url(request.url)


def reverse(endpoint, _external=False, method='GET', **values):
  """
  An utility function for jinja2.
  """
  return local.url_adapter.build(endpoint, values, method=method,
      force_external=_external)


def render_to_string(template, context={}):
  """
  A function for template rendering.
  """
  jinja2_env = getattr(local, 'jinja2_env', None)
  template = jinja2_env.get_template(template)
  return template.render(context)


def render_to_response(template, context, mimetype='text/html'):
  """
  A function for adding useful variables to context automatically, but
  none yet.
  """
  return Response(render_to_string(template, context), mimetype=mimetype)


def to_local_timezone(datetime, tzname=settings.DEFAULT_TIMEZONE):
  """Convert a datetime object to the local timezone."""
  if datetime.tzinfo is None:
    datetime = datetime.replace(tzinfo=UTC)
  tzinfo = get_timezone(tzname)
  return tzinfo.normalize(datetime.astimezone(tzinfo))


def to_utc(datetime, tzname=settings.DEFAULT_TIMEZONE):
  """Convert a datetime object to UTC and drop tzinfo."""
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
