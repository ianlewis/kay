# -*- coding: utf-8 -*-

"""
kay.nuke.urls

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/', endpoint='main', view='kay.ext.nuke.views.main_handler'),
    Rule('/delete', endpoint='delete', view='kay.ext.nuke.views.mass_delete'),
  )
]
