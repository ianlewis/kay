# -*- coding: utf-8 -*-

"""
Kay internal applications.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from werkzeug.routing import Submount, EndpointPrefix, Rule, Map
from werkzeug import Request, ClosingIterator

from kay.utils import local, local_manager
import views

def _make_url():
  return Map([
    Rule('/cron/hourly', endpoint='_kay/cron/hourly'),
    Rule('/cron/frequent', endpoint='_kay/cron/frequent'),
  ])

_views = {
  '_kay/cron/hourly': views.cron_hourly,
  '_kay/cron/frequent': views.cron_frequent,
}

class InternalApp(object):

  def __init__(self):
    self.views = _views
    self.url_map = _make_url()

  def __call__(self, environ, start_response):
    local.app = self
    local.request = request = Request(environ)
    local.url_adapter = self.url_map.bind_to_environ(environ)

    endpoint, values = local.url_adapter.match()
    response = self.views[endpoint](request, **values)

    return ClosingIterator(response(environ, start_response),
        [local_manager.cleanup])

