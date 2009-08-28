# -*- coding: utf-8 -*-

"""
Kay authentication urls.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
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
      Rule('/post_session', endpoint='post_session'),
      Rule('/logout', endpoint='logout'),
    ]),
  ]

all_views = {
  'auth/login': kay.auth.views.login,
  'auth/post_session': kay.auth.views.post_session,
  'auth/logout': kay.auth.views.logout,
}
