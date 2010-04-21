# -*- coding: utf-8 -*-

"""
kay.nuke.urls

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from werkzeug.routing import (
  Map, Rule, Submount,
  EndpointPrefix, RuleTemplate,
)

def make_rules():
  return [
    EndpointPrefix('nuke/', [
      Rule('/', endpoint='main'),
      Rule('/delete', endpoint='delete'),
    ]),
  ]

all_views = {
  'nuke/main': 'kay.ext.nuke.views.main_handler',
  'nuke/delete': 'kay.ext.nuke.views.mass_delete',
}
