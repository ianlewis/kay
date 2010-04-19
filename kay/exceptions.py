# -*- coding: utf-8 -*-

"""
Kay Exceptions

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.

Taken from django.
"""

class MiddlewareNotUsed(Exception):
  """This middleware is not used in this server configuration"""
  pass

class ImproperlyConfigured(Exception):
  """Kay is somehow improperly configured"""
  pass

class SuspiciousOperation(Exception):
  """Assumes that user did something suspicious."""
  pass

class NotAuthorized(Exception):
  """User is not permitted to do something."""
  pass
