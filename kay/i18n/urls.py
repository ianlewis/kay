# -*- coding: utf-8 -*-

"""
Kay i18n urls.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from werkzeug.routing import (
  Map, Rule, Submount,
  EndpointPrefix, RuleTemplate,
)
from kay.i18n import views

def make_rules():
  return [
    EndpointPrefix('i18n/', [
      Rule('/set_language', endpoint='set_language'),
    ]),
  ]

all_views = {
  'i18n/set_language': views.set_language,
}
