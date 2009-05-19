# -*- coding: utf-8 -*-

class NullMemcache(object):
  def get(self, name):
    return None
  def set(self, name, value, ttl):
    return None
