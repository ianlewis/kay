# -*- coding: utf-8 -*-

"""
Kay routing.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging

from werkzeug.routing import (
  EndpointPrefix, Submount
)
from werkzeug.routing import Rule as OriginalRule

class Rule(OriginalRule):
  def __init__(self, pattern, **kwargs):
    try:
      self.view = kwargs.pop('view')
    except KeyError:
      self.view = None
    OriginalRule.__init__(self, pattern, **kwargs)

class ViewGroup(object):
  add_app_prefix_to_endpoint = True
  url_prefix = None

  def __init__(self, *args, **kwargs):
    if kwargs.has_key('add_app_prefix_to_endpoint'):
      self.add_app_prefix_to_endpoint = kwargs['add_app_prefix_to_endpoint']
    if kwargs.has_key('url_prefix'):
      self.url_prefix = kwargs['url_prefix']
    self.rules = []
    self.views = {}
    for rule in args:
      if not isinstance(rule, Rule):
        continue
      self.rules.append(rule)
      if self.views.has_key(rule.endpoint):
        logging.info('An endpoint is already configured, skipped.')
      else:
        self.views[rule.endpoint] = rule.view

  def get_rules(self, app=None):
    if self.add_app_prefix_to_endpoint and app is not None:
      ret = [EndpointPrefix(app+'/', self._get_rules())]
    else:
      ret = self._get_rules()
    if self.url_prefix:
      return [Submount(self.url_prefix, ret)]
    else:
      return ret

  def get_views(self, app=None):
    if self.add_app_prefix_to_endpoint and app is not None:
      return self._get_views(app+'/')
    else:
      return self._get_views()

  def _get_views(self, prefix=None):
    if not prefix:
      return self.views
    ret = {}
    for key, val in self.views.iteritems():
      ret[prefix+key] = val
    return ret
    
  def _get_rules(self):
    return self.rules

