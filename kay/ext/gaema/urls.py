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
    Rule('/goog_openid_login', endpoint='goog_openid_login',
         view='kay.ext.gaema.views.goog_openid_login'),
    Rule('/twitter_login', endpoint='twitter_login',
         view='kay.ext.gaema.views.twitter_login'),
    Rule('/facebook_login', endpoint='facebook_login',
         view='kay.ext.gaema.views.facebook_login'),
    Rule('/goog_openid_logout', endpoint='goog_openid_logout',
         view='kay.ext.gaema.views.goog_openid_logout'),
    Rule('/twitter_logout', endpoint='twitter_logout',
         view='kay.ext.gaema.views.twitter_logout'),
    Rule('/facebook_logout', endpoint='facebook_logout',
         view='kay.ext.gaema.views.facebook_logout'),
  )
]
