# -*- coding: utf-8 -*-

"""
kay.ext.gaema.urls

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/login/<service>', endpoint='login',
         view='kay.ext.gaema.views.login'),
    Rule('/logout/<service>', endpoint='logout',
         view='kay.ext.gaema.views.logout'),
    Rule('/marketplace_login/a/<domain>', endpoint='marketplace_login',
         view='kay.ext.gaema.views.marketplace_login'),
    Rule('/marketplace_logout/<domain>', endpoint='marketplace_logout',
         view='kay.ext.gaema.views.marketplace_logout'),
    Rule('/select_service/<targets>', endpoint='select_service',
         view='kay.ext.gaema.views.select_service'),
  )
]
