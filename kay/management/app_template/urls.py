# -*- coding: utf-8 -*-
# %app_name%.urls
# 
# Following few lines is an example urlmapping with a newer interface.

"""
from kay.view_group import (
  ViewGroup, URL
)

view_groups = [
  ViewGroup(URL('/', endpoint='index', view='%app_name%.views.index'))
]
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
