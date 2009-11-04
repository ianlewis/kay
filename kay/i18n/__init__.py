# -*- coding: utf-8 -*-
"""
kay.i18n
~~~~~~~~~

Kay i18n tools.  This module provides various helpers for
internationalization.  That is a translation system (with an API,
compatible to standard gettext), timezone helpers as well as date
parsing and formatting functions.

General Architecture
--------------------

The i18n system is based on a few general principles.  Internally all
times are stored in UTC as naive datetime objects (that means no tzinfo
is present).  The internal language is American English and all text
information is stored as unicode strings.

For display strings are translated to the language of the blog and all
dates as converted to the blog timezone.

Translations are handled in a gettext inspired way via babel.  The
translatable strings are stored in POT and PO files and eventually
applications will reads translations from MO files.

Translation Workflow
--------------------

The extracting of strings is done with the `extract-messages`
script. The messages collected are stored in the `messages.pot`
file in the i18n folder of the project.

The actual translations have to be updated by hand with those strings.
The `update-translations` script will automatically add new strings to
the po files and try to do fuzzy matching.

To compile the translations into the MO files just use
`compile-translations`.

New languages are added with `add-translation`.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:copyright: (c) 2009 by the Zine Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.

This file is originally derived from Zine project.
"""

import os
from gettext import NullTranslations

import kay
from kay.utils import local
from kay.conf import settings

__all__ = ['_', 'gettext', 'ngettext', 'lazy_gettext', 'lazy_ngettext']


DATE_FORMATS = ['%m/%d/%Y', '%d/%m/%Y', '%Y%m%d', '%d. %m. %Y',
                '%m/%d/%y', '%d/%m/%y', '%d%m%y', '%m%d%y', '%y%m%d']
TIME_FORMATS = ['%H:%M', '%H:%M:%S', '%I:%M %p', '%I:%M:%S %p']


def create_lang_url(lang=None, url=None):
  from werkzeug.urls import url_quote_plus
  from kay.utils import url_for
  if not url:
    url = local.request.url
  return url_for("i18n/set_language", lang=lang, next=url_quote_plus(url))

def load_translations(locale):
  """Load the translation for a locale.  If a locale does not exist
  the return value a fake translation object.
  """
  from werkzeug.utils import import_string

  from kay.i18n.translations import KayTranslations
  from kay import utils
  domain = "messages"
  ret = KayTranslations.load(utils.get_kay_locale_path(), locale, domain)
  def _merge(path):
    t = KayTranslations.load(path, locale, domain)
    if t is not None:
      if ret is None:
        return t
      elif isinstance(ret, KayTranslations):
        ret.merge(t)
    return ret
  try:
    installed_apps = local.app.app_settings.INSTALLED_APPS
  except AttributeError:
    installed_apps = settings.INSTALLED_APPS
  for appname in installed_apps:
    app = import_string(appname)
    apppath = os.path.join(os.path.dirname(app.__file__), 'i18n')

    if os.path.isdir(apppath):
      ret = _merge(apppath)
  # Add I18N_DIR
  try:
    target = os.path.join(kay.PROJECT_DIR, local.app.app_settings.I18N_DIR)
    if os.path.isdir(target):
      ret = _merge(target)
  except AttributeError:
    pass
  return ret


class KayNullTranslations(NullTranslations):
  gettext = NullTranslations.ugettext
  ngettext = NullTranslations.ungettext

  def __init__(self, fileobj=None, locale=None):
    NullTranslations.__init__(self, fileobj)
    self.lang = locale
    self._catalog = {}

  def merge(self, translations):
    """Update the translations with others."""
    self.add_fallback(translations)

  def __nonzero__(self):
    return bool(self._fallback)


def get_translations():
  """Get the active translations or default translations."""
  try:
    ret = local.app.active_translations
    default = local.app.app_settings.DEFAULT_LANG
  except Exception:
    ret = None
    default = settings.DEFAULT_LANG
  if ret is not None:
    return ret
  return load_translations(default)

def gettext_noop(string):
  return unicode(string)

def gettext(string):
  """Translate a given string to the language of the application."""
  translations = get_translations()
  if translations is None:
    return unicode(string)
  return translations.gettext(string)


def ngettext(singular, plural, n):
  """Translate the possible pluralized string to the language of the
  application.
  """
  translations = get_translations()
  if translations is None:
    if n == 1:
      return unicode(singular)
    return unicode(plural)
  return translations.ngettext(singular, plural, n)


class _TranslationProxy(object):
  """Class for proxy strings from gettext translations.  This is a helper
  for the lazy_* functions from this module.

  The proxy implementation attempts to be as complete as possible, so that
  the lazy objects should mostly work as expected, for example for sorting.
  """
  __slots__ = ('_func', '_args')

  def __init__(self, func, *args):
    self._func = func
    self._args = args

  value = property(lambda x: x._func(*x._args))

  def __contains__(self, key):
    return key in self.value

  def __nonzero__(self):
    return bool(self.value)

  def __dir__(self):
    return dir(unicode)

  def __iter__(self):
    return iter(self.value)

  def __len__(self):
    return len(self.value)

  def __str__(self):
    return str(self.value)

  def __unicode__(self):
    return unicode(self.value)

  def __add__(self, other):
    return self.value + other

  def __radd__(self, other):
    return other + self.value

  def __mod__(self, other):
    return self.value % other

  def __rmod__(self, other):
    return other % self.value

  def __mul__(self, other):
    return self.value * other

  def __rmul__(self, other):
    return other * self.value

  def __lt__(self, other):
    return self.value < other

  def __le__(self, other):
    return self.value <= other

  def __eq__(self, other):
    return self.value == other

  def __ne__(self, other):
    return self.value != other

  def __gt__(self, other):
    return self.value > other

  def __ge__(self, other):
    return self.value >= other

  def __getattr__(self, name):
    if name == '__members__':
      return self.__dir__()
    return getattr(self.value, name)

  def __getstate__(self):
    return self._func, self._args

  def __setstate__(self, tup):
    self._func, self._args = tup

  def __getitem__(self, key):
    return self.value[key]

  def __copy__(self):
    return self

  def __repr__(self):
    try:
      return 'i' + repr(unicode(self.value))
    except Exception:
      return '<%s broken>' % self.__class__.__name__


def lazy_gettext(string):
  """A lazy version of `gettext`."""
  if isinstance(string, _TranslationProxy):
    return string
  return _TranslationProxy(gettext, string)


def lazy_ngettext(singular, plural, n):
  """A lazy version of `ngettext`"""
  return _TranslationProxy(ngettext, singular, plural, n)


def format_system_datetime(datetime=None, rebase=True):
  """Formats a system datetime.  This is the format the admin
  panel uses by default.  (Format: YYYY-MM-DD hh:mm and in the
  user timezone unless rebase is disabled)
  """

  from kay.utils import to_local_timezone
  if rebase:
    datetime = to_local_timezone(datetime)
  return u'%d-%02d-%02d %02d:%02d' % (
    datetime.year,
    datetime.month,
    datetime.day,
    datetime.hour,
    datetime.minute
  )


def parse_datetime(string, rebase=True):
  """Parses a string into a datetime object.  Per default a conversion
  from the blog timezone to UTC is performed but returned as naive
  datetime object (that is tzinfo being None).  If rebasing is disabled
  the string is expected in UTC.

  The return value is **always** a naive datetime object in UTC.  This
  function should be considered of a lenient counterpart of
  `format_system_datetime`.
  """
  from datetime import datetime
  from time import strptime

  from kay.utils import to_utc

  # shortcut: string as None or "now" or the current locale's
  # equivalent returns the current timestamp.
  if string is None or string.lower() in ('now', _('now')):
    return datetime.utcnow().replace(microsecond=0)

  def convert(format):
    """Helper that parses the string and convers the timezone."""
    rv = datetime(*strptime(string, format)[:7])
    if rebase:
      rv = to_utc(rv)
    return rv.replace(microsecond=0)

  # first of all try the following format because this is the format
  # Texpress will output by default for any date time string in the
  # administration panel.
  try:
    return convert(u'%Y-%m-%d %H:%M')
  except ValueError:
    pass

  # no go with time only, and current day
  for fmt in TIME_FORMATS:
    try:
      val = convert(fmt)
    except ValueError:
      continue
    return to_utc(datetime.utcnow().replace(hour=val.hour,
                  minute=val.minute, second=val.second, microsecond=0))

  # no try various types of date + time strings
  def combined():
    for t_fmt in TIME_FORMATS:
      for d_fmt in DATE_FORMATS:
        yield t_fmt + ' ' + d_fmt
        yield d_fmt + ' ' + t_fmt

  for fmt in combined():
    try:
      return convert(fmt)
    except ValueError:
      pass

  raise ValueError('invalid date format')


_ = gettext
