# -*- coding: utf-8 -*-

"""
Kay test urls.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from kay.generics.rest import RESTViewGroup

class MyRESTViewGroup(RESTViewGroup):
  models = [
    'kay.tests.restapp.models.RestModel',
  ]

view_groups = [
  MyRESTViewGroup(),
]
