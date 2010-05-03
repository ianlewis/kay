# -*- coding: utf-8 -*-
# %app_name%.urls
# 

# Following few lines is an example urlmapping with an older interface.
"""
from werkzeug.routing import EndpointPrefix, Rule

def make_rules():
  return [
    EndpointPrefix('%app_name%/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  '%app_name%/index': '%app_name%.views.index',
}
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='%app_name%.views.index'),
  )
]

