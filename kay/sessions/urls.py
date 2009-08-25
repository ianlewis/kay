# -*- coding: utf-8 -*-

"""
Kay sessions urls.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from werkzeug.routing import (
  Map, Rule, Submount,
  EndpointPrefix, RuleTemplate,
)
import kay.sessions.views

def make_rules():
  return [
    EndpointPrefix('sessions/', [
      Rule('/purge_old_sessions', endpoint='purge'),
    ]),
  ]

all_views = {
  'sessions/purge': kay.sessions.views.purge_old_sessions,
}
