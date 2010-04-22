# -*- coding: utf-8 -*-

"""
Kay internal urls.

:Copyright: (c) 2009 Accense Technology, Inc.,
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/cron/hourly', endpoint='cron/hourly',
         view='kay._internal.views.cron_hourly'),

    Rule('/cron/frequent', endpoint='cron/frequent',
         view='kay._internal.views.cron_frequent'),

    Rule('/expire_registration/<registration_key>',
         endpoint='expire_registration',
         view='kay._internal.views.expire_registration'),

    Rule('/expire_temporary_session/<session_key>',
         endpoint='expire_temporary_session',
         view='kay._internal.views.expire_temporary_session'),

    Rule('/send_registration_confirm/<registration_key>',
         endpoint='send_registration_confirm',
         view='kay._internal.views.send_registration_confirm'),

    Rule('/send_reset_password_instruction/<user_key>/<session_key>',
         endpoint='send_reset_password_instruction',
         view='kay._internal.views.send_reset_password_instruction'),
  )
]

