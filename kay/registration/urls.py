# -*- coding: utf-8 -*-

"""
Kay registration urls.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from werkzeug.routing import (
  Rule, EndpointPrefix,
)

def make_rules():
  return [
    EndpointPrefix('registration/', [
      Rule('/activate/<activation_key>', endpoint='activate'),
      Rule('/register', endpoint='register'),
      Rule('/registration_complete', endpoint='registration_complete'),
    ]),
  ]

all_views = {
  'registration/activate': ('kay.registration.views.ActivateHandler', (), {}),
  'registration/register': ('kay.registration.views.RegisterHandler', (), {}),
  'registration/registration_complete':
    'kay.registration.views.registration_complete',
}
