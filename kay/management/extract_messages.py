#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extract Messages
~~~~~~~~~~~~~~~~

Extract messages into a PO-Template.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:copyright: (c) 2009 by the Zine Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.

This file originally derives from Zine Project.
"""
from os import path, makedirs
import sys

import kay
kay.setup_syspath()

from babel.messages import Catalog
from babel.messages.extract import extract_from_dir
from babel.messages.pofile import write_po

from kay.management.utils import (
  print_status, get_user_apps,
)
from kay.conf import settings

KEYWORDS = {
  '__': None,
  '_': None,
  'gettext': None,
  'gettext_noop': None,
  'ngettext': (1, 2),
  'lazy_gettext': None,
  'lazy_ngettext': (1, 2),
}
BUGS_ADDRESS = 'tmatsuo@candit.jp'
COPYRIGHT = 'Takashi Matsuo'
METHODS = [
  ('**.py', 'python'),
  ('**/templates_compiled/**.*', 'ignore'),
  ('**/templates/*~', 'ignore'),
  ('**/templates/**.*', 'jinja2.ext:babel_extract'),
  ('**.html', 'jinja2.ext:babel_extract'),
  ('**.js', 'ignore'),
]
JSMETHODS = [
  ('**.py', 'ignore'),
  ('**/templates/**.html', 'ignore'),
  ('**.js', 'javascript'),
  ('**/templates_compiled/**.*', 'ignore'),
]
COMMENT_TAGS = ['_', '__', 'gettext', 'ngettext', 'lazy_gettext',
                'lazy_ngettext']


def strip_path(filename, base):
  filename = path.normpath(path.join(base, filename))
  return filename[len(path.commonprefix([
    filename, path.dirname(base)])):].lstrip(path.sep)


def do_extract_messages(target=('t', ''), domain=('d', 'messages'),
                        i18n_dir=('i', ''), all=('a', False)):
  """
  Extract messages and create pot file.
  """
  if not domain in ('messages', 'jsmessages'):
    print_status('invalid domain.')
    sys.exit(1)
  if not target and not all:
    print_status('Please specify target.')
    sys.exit(1)
  elif target == 'kay':
    print_status('Extracting core strings')
    root = kay.KAY_DIR
  elif all:
    targets = get_user_apps()
    for target in targets:
      do_extract_messages(target=target, domain=domain, i18n_dir=None,
                          all=False)
    for template_dir in settings.TEMPLATE_DIRS:
      do_extract_messages(target=template_dir, domain=domain,
                          i18n_dir=settings.I18N_DIR, all=False)
    sys.exit(0)
  else:
    root = path.abspath(target)
    if not path.isdir(root):
      print_status('source folder missing')
      sys.exit(1)
    print_status('Extracting from %s' % root)
  if domain == 'messages':
    methods = METHODS
  else:
    methods = JSMETHODS

  catalog = Catalog(msgid_bugs_address=BUGS_ADDRESS,
                    copyright_holder=COPYRIGHT, charset='utf-8')

  def callback(filename, method, options):
    if method != 'ignore':
      print_status(strip_path(filename, root))

  option = {}
  option['extensions'] = ','.join(settings.JINJA2_EXTENSIONS)
  option.update(settings.JINJA2_ENVIRONMENT_KWARGS)
  options = {
    '**/templates/**.*': option,
    '**.html': option,
  }
  extracted = extract_from_dir(root, methods, options, KEYWORDS,
                               COMMENT_TAGS, callback=callback,
                               strip_comment_tags=True)

  for filename, lineno, message, comments in extracted:
    catalog.add(message, None, [(strip_path(filename, root), lineno)],
                auto_comments=comments)
  if not i18n_dir:
    i18n_dir = path.join(root, 'i18n')
  if not path.isdir(i18n_dir):
    makedirs(i18n_dir)

  f = file(path.join(i18n_dir, domain+'.pot'), 'w')
  try:
    write_po(f, catalog, width=79)
  finally:
    f.close()

  print_status('All done.')
