# -*- coding: utf-8 -*-

"""
Kay auth application.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""


def process_context(request):
  return {'user': request.user}
