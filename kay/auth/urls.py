# -*- coding: utf-8 -*-

"""
Kay authentication urls.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/login', endpoint='login', view='kay.auth.views.login'),
    Rule('/login_box', endpoint='login_box', view='kay.auth.views.login_box'),
    Rule('/post_session', endpoint='post_session',
         view='kay.auth.views.post_session'),
    Rule('/logout', endpoint='logout', view='kay.auth.views.logout'),
    Rule('/change_password', endpoint='change_password',
         view=('kay.auth.views.ChangePasswordHandler',(), {})),
    Rule('/request_reset_password', endpoint='request_reset_password',
         view='kay.auth.views.request_reset_password'),
    Rule('/reset_password/<session_key>', endpoint='reset_password',
         view='kay.auth.views.reset_password'),
  )
]
