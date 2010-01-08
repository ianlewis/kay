# -*- coding: utf-8 -*-

"""
Kay sessions urls.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from werkzeug.routing import (
  Map, Rule, Submount,
  EndpointPrefix, RuleTemplate,
)

def make_rules():
  return [
    EndpointPrefix('sessions/', [
      Rule('/purge_old_sessions', endpoint='purge'),
    ]),
  ]

all_views = {
  'sessions/purge': 'kay.sessions.views.purge_old_sessions',
}
