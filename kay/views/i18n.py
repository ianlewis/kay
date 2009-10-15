import os

from werkzeug import Response
from werkzeug.utils import import_string

import kay
from kay.conf import settings
from kay.utils.text import javascript_quote
import gettext as gettext_module

NullSource = """
/* gettext identity library */

function gettext(msgid) { return msgid; }
function ngettext(singular, plural, count) { return (count == 1) ? singular : plural; }
function gettext_noop(msgid) { return msgid; }
"""

LibHead = """
/* gettext library */

var catalog = new Array();
"""

LibFoot = """

function gettext(msgid) {
  var value = catalog[msgid];
  if (typeof(value) == 'undefined') {
    return msgid;
  } else {
    return (typeof(value) == 'string') ? value : value[0];
  }
}

function ngettext(singular, plural, count) {
  value = catalog[singular];
  if (typeof(value) == 'undefined') {
    return (count == 1) ? singular : plural;
  } else {
    return value[pluralidx(count)];
  }
}

function gettext_noop(msgid) { return msgid; }
"""

SimplePlural = """
function pluralidx(count) { return (count == 1) ? 0 : 1; }
"""

InterPolate = r"""
function interpolate(fmt, obj, named) {
  if (named) {
    return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
  } else {
    return fmt.replace(/%s/g, function(match){return String(obj.shift())});
  }
}
"""

PluralIdx = r"""
function pluralidx(n) {
  var v=%s;
  if (typeof(v) == 'boolean') {
    return v ? 1 : 0;
  } else {
    return v;
  }
}
"""

def null_javascript_catalog(request, domain=None, packages=None):
  """
  Returns "identity" versions of the JavaScript i18n functions -- i.e.,
  versions that don't actually do anything.
  """
  return Response(NullSource + InterPolate, content_type='text/javascript')

def javascript_catalog(request, domain='jsmessages', packages=None):
  """
  Returns the selected language catalog as a javascript library.

  Receives the list of packages to check for translations in the
  packages parameter either from an infodict or as a +-delimited
  string from the request. Default is 'django.conf'.

  Additionally you can override the gettext domain for this view,
  but usually you don't want to do that, as JavaScript messages
  go to the djangojs domain. But this might be needed if you
  deliver your JavaScript source from Django templates.
  """
  if packages is None:
    packages = ['kay']
  if type(packages) in (str, unicode):
    packages = packages.split('+')
  packages = [p for p in packages if p == 'kay' or\
                p in settings.INSTALLED_APPS]
    
  t = {}
  paths = []
  locale = request.cookies.get(settings.LANG_COOKIE_NAME)
  if not locale:
    locale = (request.accept_languages.best or
              settings.DEFAULT_LANG).split('-')[0].lower()
  # first load all english languages files for defaults
  for package in packages:
    p = import_string(package)
    path = os.path.join(os.path.dirname(p.__file__), 'i18n')
    paths.append(path)
  # Add i18n_dir
  if os.path.isdir(os.path.join(kay.PROJECT_DIR, settings.I18N_DIR)):
    paths.append(os.path.join(kay.PROJECT_DIR, settings.I18N_DIR))
  # last load the currently selected language, if it isn't identical to the default.
  for path in paths:
    try:
      catalog = gettext_module.translation(domain, path, [locale])
    except IOError:
      catalog = None
    if catalog is not None:
      t.update(catalog._catalog)
  src = [LibHead]
  plural = None
  if '' in t:
    for l in t[''].split('\n'):
      if l.startswith('Plural-Forms:'):
        plural = l.split(':',1)[1].strip()
  if plural is not None:
    # this should actually be a compiled function of a typical plural-form:
    # Plural-Forms: nplurals=3; plural=n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2;
    plural = [el.strip() for el in plural.split(';') if el.strip().startswith('plural=')][0].split('=',1)[1]
    src.append(PluralIdx % plural)
  else:
    src.append(SimplePlural)
  csrc = []
  pdict = {}
  for k, v in t.items():
    if k == '':
      continue
    if type(k) in (str, unicode):
      csrc.append("catalog['%s'] = '%s';\n" % (javascript_quote(k),
                                               javascript_quote(v)))
    elif type(k) == tuple:
      if k[0] not in pdict:
        pdict[k[0]] = k[1]
      else:
        pdict[k[0]] = max(k[1], pdict[k[0]])
      csrc.append("catalog['%s'][%d] = '%s';\n" % (javascript_quote(k[0]),
                                                   k[1],
                                                   javascript_quote(v)))
    else:
      raise TypeError, k
  csrc.sort()
  for k,v in pdict.items():
    src.append("catalog['%s'] = [%s];\n" % (javascript_quote(k),
                                            ','.join(["''"]*(v+1))))
  src.extend(csrc)
  src.append(LibFoot)
  src.append(InterPolate)
  src = ''.join(src)
  return Response(src, content_type='text/javascript')
