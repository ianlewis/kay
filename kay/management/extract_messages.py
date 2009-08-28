#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extract Messages
~~~~~~~~~~~~~~~~

Extract messages into a PO-Template.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
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

from kay.management.utils import print_status

KEYWORDS = {
  '_': None,
  'gettext': None,
  'ngettext': (1, 2),
  'lazy_gettext': None,
  'lazy_ngettext': (1, 2),
}
BUGS_ADDRESS = 'tmatsuo@candit.jp'
COPYRIGHT = 'Takashi Matsuo'
METHODS = [
  ('**.py', 'python'),
  ('**/templates/*~', 'ignore'),
  ('**/templates/**.*', 'jinja2.ext:babel_extract'),
  ('**.js', 'ignore'),
  ('**/templates_compiled/**.*', 'ignore'),
]
JSMETHODS = [
  ('**.py', 'ignore'),
  ('**/templates/**.html', 'ignore'),
  ('**.js', 'javascript'),
  ('**/templates_compiled/**.*', 'ignore'),
]
COMMENT_TAGS = ['_']


def strip_path(filename, base):
  filename = path.normpath(path.join(base, filename))
  return filename[len(path.commonprefix([
    filename, path.dirname(base)])):].lstrip(path.sep)


def do_extract_messages(target=('t', ''), domain=('d', 'messages')):
  """
  Extract messages and create pot file.
  """
  if not domain in ('messages', 'jsmessages'):
    print_status('invalid domain.')
    sys.exit(1)
  if not target:
    print_status('Please specify target.')
    sys.exit(1)
  elif target == 'kay':
    print_status('Extracting core strings')
    root = kay.KAY_DIR
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

  extracted = extract_from_dir(root, methods, {}, KEYWORDS,
                               COMMENT_TAGS, callback=callback,
                               strip_comment_tags=True)

  for filename, lineno, message, comments in extracted:
    catalog.add(message, None, [(strip_path(filename, root), lineno)],
                auto_comments=comments)

  output_path = path.join(root, 'i18n')
  if not path.isdir(output_path):
    makedirs(output_path)

  f = file(path.join(output_path, domain+'.pot'), 'w')
  try:
    write_po(f, catalog, width=79)
  finally:
    f.close()

  print_status('All done.')
