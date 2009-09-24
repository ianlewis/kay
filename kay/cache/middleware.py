# -*- coding: utf-8 -*-

"""
Middleware for cache.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging

from google.appengine.api import memcache

from kay.conf import settings
import kay.cache

def get_key(url, lang):
  return "%s?lang=%s" % (url, lang)

class CacheMiddleware(object):
  def __init__(self):
    self.cache_timeout = settings.CACHE_MIDDLEWARE_SECONDS
    self.namespace = settings.CACHE_MIDDLEWARE_NAMESPACE
    self.cache_anonymous_only = settings.CACHE_MIDDLEWARE_ANONYMOUS_ONLY

  def process_response(self, request, response):
    if not request._cache_update:
      return response
    if not response.status_code == 200:
      return response
    key = get_key(request.url, request.lang)
    timeout = response.cache_control.max_age
    if timeout is None:
      timeout = self.cache_timeout
    if memcache.set(key, response, timeout, namespace=self.namespace):
      logging.debug("CacheMiddleware cache set. key: '%s', timeout: %d" %
                    (key, timeout))
    return response
    

  def process_view(self, request, view_func, **kwargs):
    request._cache_update = False
    if hasattr(view_func, kay.cache.NO_CACHE):
      return None
    if self.cache_anonymous_only:
      assert hasattr(request, 'user'), \
          ("You need to add a particular AuthenticationMiddleware "
           "before CacheMiddleware")
    if not request.method in ('GET', 'HEAD') or request.args:
      return None
    if self.cache_anonymous_only and request.user.is_authenticated():
      return None
    key = get_key(request.url, request.lang)
    response = memcache.get(key, namespace=self.namespace)
    if response:
      logging.debug("CacheMiddleware cache hit: key '%s'" % key)
      return response
    request._cache_update = True
    return None
    
  
