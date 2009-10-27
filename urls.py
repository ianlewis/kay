# -*- coding: utf-8 -*-

"""
Kay URL dispatch setting.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from werkzeug.routing import (
  Map, Rule, Submount,
  EndpointPrefix, RuleTemplate,
)

def make_url():
  return Map([
    Rule('/_ah/queue/deferred', endpoint='deferred'),
  ])

all_views = {
  'deferred': 'kay.handlers.task.task_handler',
}
