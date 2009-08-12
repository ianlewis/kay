# -*- coding: utf-8 -*-

"""
Kay authentication urls.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from werkzeug.routing import (
  Map, Rule, Submount,
  EndpointPrefix, RuleTemplate,
)
import kay.auth.views

def make_rules():
  return [
    EndpointPrefix('auth/', [
      Rule('/login', endpoint='login'),
      Rule('/logout', endpoint='logout'),
    ]),
  ]

all_views = {
  'auth/login': kay.auth.views.login,
  'auth/logout': kay.auth.views.logout,
}
