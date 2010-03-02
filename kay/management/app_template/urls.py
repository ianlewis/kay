# -*- coding: utf-8 -*-
# %app_name%.urls


from werkzeug.routing import (
  Map, Rule, Submount,
  EndpointPrefix, RuleTemplate,
)

def make_rules():
  return [
    EndpointPrefix('%app_name%/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  '%app_name%/index': '%app_name%.views.index',
}
