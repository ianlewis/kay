# -*- coding: utf-8 -*-

"""
Kay authentication views.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from werkzeug import (
  unescape, redirect, Response,
)

def login(request):
  next = request.values.get("next")
  return Response(next)

def logout(request):
  next = request.values.get("next")
  return Response(next)
