# -*- coding: utf-8 -*-
"""
Kay test management commands.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import unittest

from kay.conf import settings

def run_test():
  suite = unittest.TestSuite()
  for app_name in settings.INSTALLED_APPS:
    try:
      tests_mod = __import__("%s.tests" % app_name, fromlist=[app_name])
    except ImportError:
      pass
    else:
      suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(tests_mod))
  unittest.TextTestRunner().run(suite)

