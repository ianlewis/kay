# -*- coding: utf-8 -*-

"""
Kay URL dispatch setting.
"""

# following few lines is a urlmapping with an older interface.
"""
from werkzeug.routing import (
  Map, Rule, Submount,
  EndpointPrefix, RuleTemplate,
)

def make_url():
  return Map([
    Rule('/_ah/queue/deferred', endpoint='deferred'),
    Rule('/maintenance_page', endpoint='_internal/maintenance_page'),
  ])

all_views = {
  'deferred': 'kay.handlers.task.task_handler',
  '_internal/maintenance_page': 'kay._internal.views.maintenance_page',
}
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/_ah/queue/deferred', endpoint='deferred',
         view='kay.handlers.task.task_handler'),
    Rule('/maintenance_page', endpoint='_internal/maintenance_page',
         view='kay._internal.views.maintenance_page'),
  )
]
