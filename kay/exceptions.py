# -*- coding: utf-8 -*-
"""
Kay exceptions.
Taken from django.
"""

class MiddlewareNotUsed(Exception):
  "This middleware is not used in this server configuration"
  pass

class ImproperlyConfigured(Exception):
  "Kay is somehow improperly configured"
  pass
