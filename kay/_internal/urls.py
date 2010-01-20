# -*- coding: utf-8 -*-

"""
Kay internal urls.

:Copyright: (c) 2009 Accense Technology, Inc.,
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from werkzeug.routing import (
  Map, Rule, Submount,
  EndpointPrefix, RuleTemplate,
)

def make_rules():
  return [
    EndpointPrefix('_internal/', [
      Rule('/cron/hourly', endpoint='cron/hourly'),
      Rule('/cron/frequent', endpoint='cron/frequent'),
      Rule('/expire_registration/<registration_key>',
           endpoint='expire_registration'),
      Rule('/expire_temporary_session/<session_key>',
           endpoint='expire_temporary_session'),
      Rule('/send_registration_confirm/<registration_key>',
           endpoint='send_registration_confirm'),
      Rule('/send_reset_password_instruction/<user_key>/<session_key>',
           endpoint='send_reset_password_instruction'),
    ]),
  ]

all_views = {
  '_internal/cron/hourly': 'kay._internal.views.cron_hourly',
  '_internal/cron/frequent': 'kay._internal.views.cron_frequent',
  '_internal/expire_registration': 'kay._internal.views.expire_registration',
  '_internal/expire_temporary_session':
    'kay._internal.views.expire_temporary_session',
  '_internal/send_registration_confirm':
    'kay._internal.views.send_registration_confirm',
  '_internal/send_reset_password_instruction':
    'kay._internal.views.send_reset_password_instruction',
}
