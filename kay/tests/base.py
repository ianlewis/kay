#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Kay test base class.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import os
import sys

def get_env():
  env = dict(os.environ)
  env['wsgi.input'] = sys.stdin
  env['wsgi.errors'] = sys.stderr
  env['wsgi.version'] = "1.0"
  env['wsgi.run_once'] = True
  env['wsgi.url_scheme'] = 'http'
  env['wsgi.multithread']  = False
  env['wsgi.multiprocess'] = True
  return env
