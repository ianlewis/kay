#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extract Messages
~~~~~~~~~~~~~~~~

Extract messages into a PO-Template.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
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

KEYWORDS = {
  '_': None,
  'gettext': None,
  'ngettext': (1, 2),
  'lazy_gettext': None,
  'lazy_ngettext': (1, 2)
}
BUGS_ADDRESS = 'tmatsuo@candit.jp'
COPYRIGHT = 'Takashi Matsuo'
METHODS = [
  ('**.py', 'python'),
  ('**/templates/**.html', 'jinja2.ext:babel_extract'),
  ('**.js', 'javascript'),
  ('**/templates_compiled/**.*', 'ignore'),
]
COMMENT_TAGS = ['_']


def strip_path(filename, base):
  filename = path.normpath(path.join(base, filename))
  return filename[len(path.commonprefix([
    filename, path.dirname(base)])):].lstrip(path.sep)


def do_extract_messages(target=''):
  if not target:
    print 'Extracting core strings'
    root = kay.KAY_DIR
  else:
    root = path.abspath(target)
    if not path.isdir(root):
      parser.error('source folder missing')
    print 'Extracting from', root

  catalog = Catalog(msgid_bugs_address=BUGS_ADDRESS,
                    copyright_holder=COPYRIGHT, charset='utf-8')

  def callback(filename, method, options):
    if method != 'ignore':
      print strip_path(filename, root)

  extracted = extract_from_dir(root, METHODS, {}, KEYWORDS,
                               COMMENT_TAGS, callback=callback,
                               strip_comment_tags=True)

  for filename, lineno, message, comments in extracted:
    catalog.add(message, None, [(strip_path(filename, root), lineno)],
                auto_comments=comments)

  output_path = path.join(root, 'i18n')
  if not path.isdir(output_path):
    makedirs(output_path)

  f = file(path.join(output_path, 'messages.pot'), 'w')
  try:
    write_po(f, catalog, width=79)
  finally:
    f.close()

  print 'All done.'
