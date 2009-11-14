#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Kay decorator test.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import unittest
import re

from werkzeug import BaseResponse, Client, Request

import kay
from kay.app import get_application
from kay.conf import LazySettings
from kay.tests import capability_stub as mocked_capability_stub

class MaintenanceCheckTestCase(unittest.TestCase):

  def setUp(self):
    s = LazySettings(settings_module='kay.tests.settings')
    app = get_application(settings=s)
    self.client = Client(app, BaseResponse)

  def tearDown(self):
    pass

  def test_redirect(self):
    """Test with normal CapabilityServiceStub"""
    response = self.client.get('/oldpage', follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, "New")
    

if __name__ == "__main__":
  unittest.main()
