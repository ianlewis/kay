#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compile translations
~~~~~~~~~~~~~~~~~~~~

Compile translations into the translated messages.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
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

from kay.management.utils import (
  print_status, get_user_apps,
)

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


def do_compile_translations(target=("t", ""), i18n_dir=("i", ""),
                            all=("a", False)):
  """
  Compiling all the templates in specified application.
  """
  if not target and not all:
    print_status('Please specify target.')
    sys.exit(1)
  elif target == 'kay':
    print_status('Compiling builtin languages')
    root = path.join(kay.KAY_DIR, 'i18n')
  elif all:
    targets = get_user_apps()
    for target in targets:
      do_compile_translations(target=target, i18n_dir=None, all=False)
    sys.exit(0)
  else:
    if i18n_dir:
      root = i18n_dir
    else:
      root = path.join(target, 'i18n')
    if not path.isdir(root):
      print('i18n folder missing')
      sys.exit(1)
    print_status('Compiling %s' % root)

  for domain in domains:
    for lang in listdir(root):
      folder = path.join(root, lang)
      translations = path.join(folder, 'LC_MESSAGES', domain+'.po')

      if path.isfile(translations):
        mo_file = open(translations.replace('.po', '.mo'), 'wb')
        print_status('Compiling %s ' % translations)
        f = file(translations)
        try:
          catalog = read_po(f, locale=lang)
        finally:
          f.close()
        # Write standard catalog
        write_mo(mo_file, catalog)
        mo_file.close()
  print_status('All done.')
