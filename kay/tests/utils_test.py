# -*- coding: utf-8 -*-

"""
Kay tests for utility functions.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging
import unittest

import simplejson

from kay.utils import (
  render_json_response,
)
from kay.utils.repr import dump

class RenderFuncTestCase(unittest.TestCase):
  KIND_NAME_UNSWAPPED = False
  USE_PRODUCTION_STUBS = True
  CLEANUP_USED_KIND = True

  def setUp(self):
    self.test_values = [
      {"foo": "foo", "bar": "foo"},
      {"foo": u"ほげ", "bar": u"ふが"},
    ]
    
  def test_render_json_response_simple(self):
    """Test for render_json_response"""
    for v in self.test_values:
      response = render_json_response(v)
      self.assertEqual(response.status_code, 200)
      v2 = simplejson.loads(response.data)
      self.assertEqual(v, v2)
