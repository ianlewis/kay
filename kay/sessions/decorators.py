# -*- coding: utf-8 -*-

"""
Kay session decorators

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import kay.sessions

def no_session(func):
  """
  This is a decortor for marking particular view not to use session.
  """
  setattr(func, kay.sessions.NO_SESSION, True)
  return func
