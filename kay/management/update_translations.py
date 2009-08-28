#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Update the translations
~~~~~~~~~~~~~~~~~~~~~~~

Update the translations from the POT.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:copyright: (c) 2009 by the Zine Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.

This file originally derives from Zine Project.
"""
from os import path, listdir, rename
import sys

import kay
kay.setup_syspath()

from babel import Locale
from babel.messages import Catalog
from babel.messages.pofile import write_po, read_po

from kay.management.utils import print_status

domains = ['messages', 'jsmessages']

def do_update_translations(target=("t", ""), lang=("l", ""),
                           statistics=("s", False)):
  """
  Update existing translations with updated pot files.
  """
  if not target:
    print_status('Please specify target.')
    sys.exit(1)
  elif target == 'kay':
    print_status('Updating core strings')
    root = path.join(kay.KAY_DIR, 'i18n')
  else:
    root = path.join(target, 'i18n')
    if not path.isdir(root):
      print_status('source folder missing')
      sys.exit(1)
    print_status('Updating %s' % root)

  for domain in domains:
    if lang:
      filepath = path.join(root, lang, 'LC_MESSAGES', domain+'.po')
      if not path.exists(filepath):
        print_status("unknown locale. %s not found." % filepath)
        sys.exit(1)
    try:
      f = file(path.join(root, domain+'.pot'))
    except IOError:
      print_status('Can not open file: %s, skipped.' %
                   path.join(root, domain+'.pot'))
      continue
    try:
      template = read_po(f)
    finally:
      f.close()

    po_files = []
    for lang_dir in listdir(root):
      filename = path.join(root, lang_dir, 'LC_MESSAGES', domain+'.po')
      if lang and filename != \
                         path.join(root, lang, 'LC_MESSAGES', domain+'.po'):
        continue
      if path.exists(filename):
        print_status('Updating %r' % lang_dir, nl=False)
        locale = Locale.parse(lang_dir)
        f = file(filename)
        try:
          catalog = read_po(f, locale=locale, domain=domain)
        finally:
          f.close()
        catalog.update(template)

        # XXX: this is kinda dangerous, but as we are using a
        # revision control system anyways that shouldn't make
        # too many problems
        f = file(filename, 'w')
        try:
          write_po(f, catalog, ignore_obsolete=True,
                   include_previous=False, width=79)
        finally:
          if statistics:
            translated = fuzzy = percentage = 0
            for message in list(catalog)[1:]:
              if message.string:
                translated +=1
              if 'fuzzy' in message.flags:
                fuzzy += 1
            if len(catalog):
              percentage = translated * 100 // len(catalog)
              print_status("-> %d of %d messages (%d%%) translated" % (
                translated, len(catalog), percentage), nl=False)
              if fuzzy:
                if fuzzy == 1:
                  print_status("%d of which is fuzzy" % fuzzy, nl=False)
                else:
                  print_status("%d of which are fuzzy" % fuzzy, nl=False)
              print_status()
          else:
            print_status()
          f.close()

  print_status('All done.')
