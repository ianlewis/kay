# -*- coding: utf-8 -*-

"""
Kay tests for utility functions.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging

import simplejson

from kay.utils import (
  render_json_response,
)
from kay.utils.repr import dump
from kay.ext.testutils.gae_test_base import GAETestBase
from kay.tests.models import JsonTestModel
from kay.dbutils import to_dict

class RenderFuncTestCase(GAETestBase):
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

class DumpModelTestCase(GAETestBase):
  KIND_NAME_UNSWAPPED = False
  USE_PRODUCTION_STUBS = True
  CLEANUP_USED_KIND = True

  def setUp(self):
    self.m1 = JsonTestModel(s="string1", i=1, b=True, l=["foo1","bar1"])
    self.m1.put()
    self.m2 = JsonTestModel(s="string2", i=2, b=False, l=["foo2","bar2"],
                            r=self.m1)
    self.m2.put()
  
  def test_to_dict(self):
    d1 = to_dict(self.m1)
    d2 = to_dict(self.m2)
    self.assertEqual(d1["s"], self.m1.s)
    self.assertEqual(d1["i"], self.m1.i)
    self.assertEqual(d1["b"], self.m1.b)
    self.assertEqual(d1["l"], self.m1.l)
    self.assertEqual(d2["r"], d1)
