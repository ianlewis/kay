# -*- coding: utf-8 -*-

"""
Kay URL dispatch setting.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from werkzeug.routing import (
  Map, Rule, Submount,
  EndpointPrefix, RuleTemplate,
)

def make_url():
  return Map([
  ])

all_views = {
}
