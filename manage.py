#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Kay management script.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import sys
import os
import logging

sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path
import kay
kay.setup_env(manage_py_env=True)
from werkzeug import script
from kay.management import *

if __name__ == '__main__':
  if len(sys.argv) == 1:
    sys.argv.append("--help")
  script.run()
