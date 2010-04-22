# -*- coding: utf-8 -*-

"""
Kay i18n urls.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/set_language', endpoint='set_language',
         view='kay.i18n.views.set_language'),
  )
]

