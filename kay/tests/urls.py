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
      Rule('/index2', endpoint='index2'),
      Rule('/no_decorator', endpoint='no_decorator'),
      Rule('/oldpage', endpoint='oldpage', redirect_to='newpage'),
      Rule('/newpage', endpoint='newpage'),
    ]),
  ]

all_views = {
  'tests/oldpage': kay.tests.views.oldpage,
  'tests/newpage': kay.tests.views.newpage,
  'tests/index': kay.tests.views.index,
  'tests/index2': kay.tests.views.index2,
  'tests/no_decorator': kay.tests.views.no_decorator,
}
