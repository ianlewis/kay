# -*- coding: utf-8 -*-

"""
Kay generics.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging

from werkzeug.routing import (
  Rule, EndpointPrefix
)

class URL(object):
  __slots__ = ('rule', 'view')
  def __init__(self, pattern, **kwargs):
    try:
      view = kwargs.pop('view')
    except KeyError:
      view = None
    self.rule = Rule(pattern, **kwargs)
    self.view = view

class ViewGroup(object):
  add_app_prefix_to_endpoint = True

  def __init__(self, *args):
    self.rules = []
    self.views = {}
    for url in args:
      if not isinstance(url, URL):
        continue
      self.rules.append(url.rule)
      if self.views.has_key(url.rule.endpoint):
        logging.info('An endpoint is already configured, skipped.')
      else:
        self.views[url.rule.endpoint] = url.view

  def get_rules(self, app):
    if self.add_app_prefix_to_endpoint:
      return [EndpointPrefix(app+'/', self._get_rules())]
    else:
      return self._get_rules()

  def get_views(self, app):
    if self.add_app_prefix_to_endpoint:
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

