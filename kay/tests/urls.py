# -*- coding: utf-8 -*-

"""
Kay test urls.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from werkzeug.routing import (
  Map, Rule, Submount,
  EndpointPrefix, RuleTemplate,
)
import kay.tests.views

def make_rules():
  return [
    EndpointPrefix('tests/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  'tests/index': kay.tests.views.index,
}
