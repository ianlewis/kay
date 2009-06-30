#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kay add_translations management script.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This script adds a new translation to Kay or Kay application.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:copyright: (c) 2009 by the Zine Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.

This file originally derives from Zine Project.
"""

from os import makedirs, path
from os.path import dirname, join, realpath, pardir, isdir, isfile
import sys

import kay
kay.setup_syspath()

from datetime import datetime
from babel import Locale, UnknownLocaleError
from babel.messages import Catalog
from babel.messages.pofile import read_po, write_po
from babel.util import LOCALTZ

domains = ['messages', 'jsmessages']

def do_add_translations(app=("a", ""), lang=("l", ""), force=("f", False)):
  try:
    locale = Locale.parse(lang)
  except (UnknownLocaleError, ValueError), e:
    print "You must specify lang."
    sys.exit()
  if app:
    add_translations(locale, join(app, 'i18n'), force)
  else:
    i18n_dir = join(kay.KAY_DIR, 'i18n')
    add_translations(locale, i18n_dir, force)


def create_from_pot(locale, path):
  try:
    f = file(path)
  except IOError, e:
    parser.error(str(e))
  try:
    catalog = read_po(f, locale=locale)
  finally:
    f.close()
  catalog.locale = locale
  catalog.revision_date = datetime.now(LOCALTZ)
  return catalog


def write_catalog(catalog, folder, domain, force):
  target = join(folder, str(catalog.locale), 'LC_MESSAGES')
  if not isdir(target):
    makedirs(target)
  filename = join(target, domain+'.po')
  if isfile(filename) and not force:
    print "%s already exists, skipped." % filename
    return
  print "Creating %s." % filename
  f = file(filename, 'w')
  try:
    write_po(f, catalog, width=79)
  finally:
    f.close()


def add_translations(locale, i18n_dir, force):
  for domain in domains:
    pot_file = join(i18n_dir, domain+'.pot')
    catalog = create_from_pot(locale, pot_file)
    write_catalog(catalog, i18n_dir, domain, force)
  print 'Created catalog for %s' % locale