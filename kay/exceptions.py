# -*- coding: utf-8 -*-

"""
Kay Exceptions

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.

Taken from django.
"""

class MiddlewareNotUsed(Exception):
  "This middleware is not used in this server configuration"
  pass

class ImproperlyConfigured(Exception):
  "Kay is somehow improperly configured"
  pass
