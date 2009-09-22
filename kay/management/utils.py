# -*- coding: utf-8 -*-

"""
Kay framework.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import sys

def print_status(msg='',nl=True):
  if nl:
    print(msg)
  else:
    print(msg),
  sys.stdout.flush()
