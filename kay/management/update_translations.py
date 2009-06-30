#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Update the translations
~~~~~~~~~~~~~~~~~~~~~~~

Update the translations from the POT.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
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

domains = ['messages', 'jsmessages']

def do_update_translations(app=("a", ""), lang=("l", ""),
                           statistics=("s", False)):
  if not app:
    print 'Updating core strings'
    root = path.join(kay.KAY_DIR, 'i18n')
  else:
    root = path.join(app, 'i18n')
    if not path.isdir(root):
      parser.error('source folder missing')
    print 'Updating', root

  for domain in domains:
    if lang:
      filepath = path.join(root, lang, 'LC_MESSAGES', domain+'.po')
      if not path.exists(filepath):
        print ("unknown locale. %s not found." % filepath)
        sys.exit(1)

    f = file(path.join(root, domain+'.pot'))
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
        print 'Updating %r' % lang_dir,
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
              print "-> %d of %d messages (%d%%) translated" % (
                translated, len(catalog), percentage),
              if fuzzy:
                if fuzzy == 1:
                  print "%d of which is fuzzy" % fuzzy,
                else:
                  print "%d of which are fuzzy" % fuzzy,
              print
          else:
            print
          f.close()

  print 'All done.'
