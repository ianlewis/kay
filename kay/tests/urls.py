# -*- coding: utf-8 -*-

"""
Kay test urls.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='kay.tests.views.index'),
    Rule('/countup', endpoint='countup', view='kay.tests.views.countup'),
    Rule('/index2', endpoint='index2', view='kay.tests.views.index2'),
    Rule('/no_decorator', endpoint='no_decorator',
         view='kay.tests.views.no_decorator'),
    Rule('/oldpage', endpoint='oldpage', redirect_to='newpage',
         view='kay.tests.views.oldpage'),
    Rule('/newpage', endpoint='newpage', view='kay.tests.views.newpage'),
  )
]
