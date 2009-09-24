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
      Rule('/maintenance_page', endpoint='maintenance_page'),
    ]),
  ]

all_views = {
  '_internal/cron/hourly': 'kay._internal.views.cron_hourly',
  '_internal/cron/frequent': 'kay._internal.views.cron_frequent',
  '_internal/maintenance_page': 'kay._internal.views.maintenance_page',
}
