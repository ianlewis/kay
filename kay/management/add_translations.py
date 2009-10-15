#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Kay add_translations management script.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This script adds a new translation to Kay or Kay application.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
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

from kay.management.utils import (
  print_status, get_user_apps,
)

domains = ['messages', 'jsmessages']

def do_add_translations(target=("t", ""), lang=("l", ""), force=("f", False),
                        i18n_dir=("i", ""), all=("a", False)):
  """
  Add new translations for specified language.
  """
  try:
    locale = Locale.parse(lang)
  except (UnknownLocaleError, ValueError), e:
    print_status("You must specify lang.")
    sys.exit(1)
  if not target and not all:
    print_status("Please specify target.")
    sys.exit(1)
  elif target == 'kay':
    i18n_dir = join(kay.KAY_DIR, 'i18n')
    add_translations(locale, i18n_dir, force)
  elif all:
    targets = get_user_apps()
    for target in targets:
      do_add_translations(target=target, lang=lang, force=force,
                          i18n_dir=None, all=False)
    sys.exit(0)
  else:
    if not i18n_dir:
      i18n_dir = join(target, 'i18n')
    add_translations(locale, i18n_dir, force)


def create_from_pot(locale, path):
  try:
    f = file(path)
  except IOError, e:
    print_status("Cant open file. Skipped %s." % path)
    return None
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
    print_status("%s already exists, skipped." % filename)
    return
  print_status("Creating %s." % filename)
  f = file(filename, 'w')
  try:
    write_po(f, catalog, width=79)
  finally:
    f.close()


def add_translations(locale, i18n_dir, force):
  for domain in domains:
    pot_file = join(i18n_dir, domain+'.pot')
    catalog = create_from_pot(locale, pot_file)
    if catalog:
      write_catalog(catalog, i18n_dir, domain, force)
  print_status('Created catalog for %s' % locale)
