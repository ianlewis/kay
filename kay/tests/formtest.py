#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import unittest

g_path = "/usr/local/google_appengine"
extra_path = [
  g_path,
  os.path.join(g_path, 'lib', 'antlr3'),
  os.path.join(g_path, 'lib', 'webob'),
  os.path.join(g_path, 'lib', 'django'),
  os.path.join(g_path, 'lib', 'yaml', 'lib')
]
sys.path = extra_path + sys.path
APP_ID = u'test'
os.environ['APPLICATION_ID'] = APP_ID

from google.appengine.ext import db
import kay
from werkzeug import Request

from kay.utils import local
from kay.utils import forms
from kay.utils.forms import ValidationError

from base import GAETestBase

class TestModel(db.Model):
  number = db.IntegerProperty()
  data = db.StringProperty()
  is_active = db.BooleanProperty()
  
class TestForm(forms.Form):
  csrf_protected = False
  username = forms.TextField("user name", required=True)
  password = forms.TextField("password", required=True)
  password_again = forms.TextField("confirm password", required=True)
  model_field = forms.ModelField(TestModel, label="ModelField Test",
                                 required=True,
                                 query=TestModel.all().filter('is_active =', True),
                                 option_name='data')
  
  def context_validate(self, data):
    if data['password'] != data['password_again']:
      raise ValidationError(u'The two passwords must be the same')

class FormTest(GAETestBase):
  def setUp(self):
    super(FormTest, self).setUp()
    if TestModel.all().count() == 0:
      for i in range(10):
        t = TestModel(number=i, data='Test Data %02d' % i, is_active=(i%2==0))
        t.put()

  def test_form(self):
    """Form validation test with context_validate."""
    os.environ['REQUEST_METHOD'] = 'POST'
    local.request = Request(self.get_env())
    f = TestForm()
    params = {'username': 'hoge'}
    self.assertEqual(f.validate(params), False)
    params = {
      'username': 'hoge',
      'password': 'fugafuga',
      'password_again': 'fugafuga',
      'model_field': str(TestModel.all().get().key())
    }
    result = f.validate(params)
    self.assertEqual(result, True)
    params['password_again'] = 'moge'
    result = f.validate(params)
    self.assertEqual(result, False)

  def tearDown(self):
    entries = TestModel.all().fetch(100)
    db.delete(entries)

class TestForm2(forms.Form):
  csrf_protected = False
  int_field = forms.IntegerField("int", min_value=5, max_value=99)
  float_field = forms.FloatField("float", min_value=5.5, max_value=99.9)
  number_field = forms.NumberField("number", min_value=5.5, max_value=99.9)

class NumberFieldTest(GAETestBase):
  def setUp(self):
    super(NumberFieldTest, self).setUp()
    os.environ['REQUEST_METHOD'] = 'POST'
    local.request = Request(self.get_env())

  def test_validate(self):
    """Float value validation test."""
    f = TestForm2()
    result = f.validate({'float_field': 10.7})
    self.assertEqual(result, True)
    self.assertEqual(f['float_field'], 10.7)

    f = TestForm2()
    result = f.validate({'float_field': 'ten'})
    self.assertEqual(result, False)

    f = TestForm2()
    result = f.validate({'number_field': 10.7})
    self.assertEqual(result, True)
    self.assertEqual(f['number_field'], 10.7)

    f = TestForm2()
    result = f.validate({'number_field': 'ten'})
    self.assertEqual(result, False)

    f = TestForm2()
    result = f.validate({'int_field': 10})
    self.assertEqual(result, True)
    self.assertEqual(f['int_field'], 10)

    f = TestForm2()
    result = f.validate({'int_field': 'ten'})
    self.assertEqual(result, False)

  def test_min(self):
    """Minimal value validation test."""
    f = TestForm2()
    result = f.validate({'float_field': 5.4})
    self.assertEqual(result, False)

    result = f.validate({'int_field': 4})
    self.assertEqual(result, False)

    result = f.validate({'number_field': 5.4})
    self.assertEqual(result, False)

  def test_max(self):
    """Maximum value validation test."""
    f = TestForm2()
    result = f.validate({'float_field': 100.1})
    self.assertEqual(result, False)

    result = f.validate({'int_field': 100})
    self.assertEqual(result, False)

    result = f.validate({'number_field': 100.1})
    self.assertEqual(result, False)


if __name__ == "__main__":
  unittest.main()
