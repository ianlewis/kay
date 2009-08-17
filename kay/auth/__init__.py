# -*- coding: utf-8 -*-

"""
Kay auth application.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""


def process_context(request):
  return {'user': request.user}
