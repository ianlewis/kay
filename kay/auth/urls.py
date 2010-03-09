# -*- coding: utf-8 -*-

"""
Kay authentication urls.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from werkzeug.routing import (
  Rule, EndpointPrefix,
)

def make_rules():
  return [
    EndpointPrefix('auth/', [
      Rule('/login', endpoint='login'),
      Rule('/login_box', endpoint='login_box'),
      Rule('/post_session', endpoint='post_session'),
      Rule('/logout', endpoint='logout'),
      Rule('/change_password', endpoint='change_password'),
      Rule('/request_reset_password', endpoint='request_reset_password'),
      Rule('/reset_password/<session_key>', endpoint='reset_password'),
    ]),
  ]

all_views = {
  'auth/login_box': 'kay.auth.views.login_box',
  'auth/login': 'kay.auth.views.login',
  'auth/post_session': 'kay.auth.views.post_session',
  'auth/logout': 'kay.auth.views.logout',
  'auth/change_password': ('kay.auth.views.ChangePasswordHandler',(), {}),
  'auth/request_reset_password': 'kay.auth.views.request_reset_password',
  'auth/reset_password': 'kay.auth.views.reset_password',
}
