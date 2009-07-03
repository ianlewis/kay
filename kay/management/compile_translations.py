#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compile translations
~~~~~~~~~~~~~~~~~~~~

Compile translations into the translated messages.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:copyright: (c) 2009 by the Zine Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.

This file originally derives from Zine Project.
"""
import pickle
import struct
from os import listdir, path
import sys

import kay
kay.setup_syspath()

from optparse import OptionParser
from babel.messages.pofile import read_po
from babel.messages.mofile import write_mo

domains = ['messages', 'jsmessages']

def is_untranslated(obj):
  if not obj:
    return True
  elif isinstance(obj, basestring):
    return not obj.strip()
  for translation in obj:
    if translation.strip():
      return False
  return True


def do_compile_translations(app=("a", "")):
  """
  Compiling all the templates in specified application.
  """
  if not app:
    print 'Please specify app.'
    sys.exit(1)
  elif app == 'kay':
    print 'Compiling builtin languages'
    root = path.join(kay.KAY_DIR, 'i18n')
  else:
    root = path.join(app, 'i18n')
    if not path.isdir(root):
      print('i18n folder missing')
      sys.exit(1)
    print 'Compiling', root

  for domain in domains:
    for lang in listdir(root):
      folder = path.join(root, lang)
      translations = path.join(folder, 'LC_MESSAGES', domain+'.po')

      if path.isfile(translations):
        mo_file = open(translations.replace('.po', '.mo'), 'wb')
        print 'Compiling %r ' % lang,
        f = file(translations)
        try:
          catalog = read_po(f, locale=lang)
        finally:
          f.close()
        # Write standard catalog
        write_mo(mo_file, catalog)
        mo_file.close()
  print 'All done.'
