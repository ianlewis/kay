# -*- coding: utf-8 -*-
# %app_name%.urls

"""
Bellow is an easy example to mount this %app_name% application.

------------------------------------
from %app_name% import urls as %app_name%_urls

def make_url():
  return Map([
    Submount('/%app_name%', %app_name%_urls.make_rules())
  ])

all_views = {
}
all_views.update(%app_name%_urls.all_views)

------------------------------------

"""

from werkzeug.routing import (
  Map, Rule, Submount,
  EndpointPrefix, RuleTemplate,
)
import %app_name%.views

def make_rules():
  return [
    EndpointPrefix('%app_name%/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  '%app_name%/index': %app_name%.views.index,
}
