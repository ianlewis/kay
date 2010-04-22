# -*- coding: utf-8 -*-

"""
Kay registration urls.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/activate/<activation_key>', endpoint='activate',
         view=('kay.registration.views.ActivateHandler', (), {})),
    Rule('/register', endpoint='register',
         view=('kay.registration.views.RegisterHandler', (), {})),
    Rule('/registration_complete', endpoint='registration_complete',
         view='kay.registration.views.registration_complete'),
  )
]

