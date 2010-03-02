import os

from babel.support import Translations as TranslationsBase

class KayTranslations(TranslationsBase):
  gettext = TranslationsBase.ugettext
  ngettext = TranslationsBase.ungettext

  def __init__(self, fileobj=None, locale=None):
    self.lang = locale
    self._catalog = {}
    TranslationsBase.__init__(self, fileobj=fileobj)
    if not hasattr(self, "plural"):
      self.plural = lambda n: int(n != 1)


  @classmethod
  def load(cls, path, locale=None, domain='messages'):
    """Load the translations from the given path."""
    from babel.core import parse_locale
    lang, script, territory, variant = parse_locale(locale)
    parsed_locale = '_'.join(filter(None, [lang, script, territory, variant]))
    catalog = os.path.join(path, parsed_locale, 'LC_MESSAGES', domain + '.mo')
    if os.path.isfile(catalog):
      return KayTranslations(fileobj=open(catalog, 'rb'), locale=locale)
    else:
      return KayTranslations(fileobj=None, locale=locale)

  def merge(self, other):
    self._catalog.update(other._catalog)

  def __nonzero__(self):
    return bool(self._catalog)
