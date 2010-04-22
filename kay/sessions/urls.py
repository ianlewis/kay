# -*- coding: utf-8 -*-

"""
Kay sessions urls.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/purge_old_sessions', endpoint='purge',
         view='kay.sessions.views.purge_old_sessions'),
  )
]
