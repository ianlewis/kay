#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for forms.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import sys
import os
import unittest
import logging

from google.appengine.ext import db
import kay
kay.setup()
from kay.misc import get_appid

APP_ID = get_appid()
os.environ['APPLICATION_ID'] = APP_ID

from werkzeug import Request

from kay.utils import local
from kay.utils import forms
from kay.utils.forms import ValidationError
from kay.tests.models import (
  TestModel, TestModel2, TestModelForm, ModelFormTestModel, ModelFormTestForm,
  ValidationTestForm,
)
from kay.tests.utils import get_env
from kay.ext.testutils.gae_test_base import GAETestBase


class ModelFormTest(GAETestBase):
  KIND_NAME_UNSWAPPED = False
  USE_PRODUCTION_STUBS = True
  CLEANUP_USED_KIND = True

  def setUp(self):
    os.environ['REQUEST_METHOD'] = 'POST'
    local.request = Request(get_env())

  def test_context_validate(self):
    f = ValidationTestForm()
    f.validate({"slist": 'hoge fuga'})
    w = f.as_widget()
    w()

  def test_override(self):
    e1 = ModelFormTestModel(s_name='s_name', zip_code='1111111', addr='addr')
    e1.put()
    f = ModelFormTestForm(instance=e1)
    f.validate({"s_name": "hoge"})
    f.save()
    e2 = ModelFormTestModel.all().get()
    self.assertEqual(e2.s_name, "hoge")
    self.assertEqual(e2.zip_code, "1111111")
    self.assertEqual(e2.addr, "addr")

  def test_form(self):
    """Test for modifying existing entity with ModelForm."""

    # first create a new entity
    f = TestModelForm()
    params = {"number": "12", "data_field": "data string",
              "is_active": "False", "string_list_field": "list"}
    self.assertEqual(f.validate(params), True)
    f.save()
    self.assertEqual(TestModel.all().count(), 1)
    entity = TestModel.all().get()
    self.assertEqual(entity.number, 12)

    # modify with TestModelForm
    f = TestModelForm(instance=entity)
    params = {"number": "13", "data_field": "modified data",
              "is_active": "True", "string_list_field": "line 1\nline 2"}
    self.assertEqual(f.validate(params), True)
    f.save()

    # check values
    self.assertEqual(TestModel.all().count(), 1)
    entity = TestModel.all().get()
    self.assertEqual(entity.number, 13)
    self.assertEqual(entity.data_field, "modified data")
    self.assertEqual(entity.is_active, True)
    self.assertEqual(entity.string_list_field, ["line 1", "line 2"])

    """Form validation test with ModelForm."""
    os.environ['REQUEST_METHOD'] = 'POST'
    local.request = Request(get_env())
    f = TestModelForm()
    params = {"number": "12"}
    # In your view, you can validate the form data with:
    # f.validate(request.form)
    # or with(If you have FileField):
    # f.validate(request.form, request.files)
    self.assertEqual(f.validate(params), False)
    f.reset()
    params = {"number": "12",
              "data_field": "data string longer than 20 characters",
              "is_active": "False",
              "string_list_field": "test"}
    self.assertEqual(f.validate(params), False)

    f.reset()
    params = {"number": "12",
              "data_field": "data string",
              "is_active": "False",
              "string_list_field": ""}
    self.assertEqual(f.validate(params), False)

    # create a new entity
    f.reset()
    params = {"number": "12", "data_field": "data string",
              "is_active": "False", "string_list_field": "list"}
    self.assertEqual(f.validate(params), True)
    f.save()
    self.assertEqual(TestModel.all().count(), 2)
    

  def tearDown(self):
    pass

class TestForm(forms.Form):
  csrf_protected = False
  username = forms.TextField("user name", required=True)
  password = forms.TextField("password", required=True)
  password_again = forms.TextField("confirm password", required=True)
  model_field = forms.ModelField(TestModel2, label="ModelField Test",
                                 required=True,
                                 option_name='data_field')
  string_list_field = forms.LineSeparated(forms.TextField(),
                                          "string list field", required=True)

  def context_validate(self, data):
    if data['password'] != data['password_again']:
      raise ValidationError(u'The two passwords must be the same')

class FormTest(GAETestBase):
  KIND_NAME_UNSWAPPED = False
  USE_PRODUCTION_STUBS = True
  CLEANUP_USED_KIND = True

  def setUp(self):
    if TestModel2.all().count() == 0:
      def txn(d):
        e = TestModel2(**d)
        e.put()
      for i in range(10):
        db.run_in_transaction(
          txn,
          dict(number=i, data_field='Test Data %02d' % i, is_active=(i%2==0)))


  def test_form(self):
    """Form validation test with context_validate."""
    os.environ['REQUEST_METHOD'] = 'POST'
    local.request = Request(get_env())
    f = TestForm()
    f.model_field.set_query(TestModel2.all().filter('is_active =', True))
    params = {'username': 'hoge'}
    self.assertEqual(f.validate(params), False)
    params = {
      'username': 'hoge',
      'password': 'fugafuga',
      'password_again': 'fugafuga',
      'string_list_field': 'hoge',
      'model_field': str(TestModel2.all().filter('is_active =', True).get().key())
    }
    result = f.validate(params)
    self.assertEqual(result, True)

    params['password_again'] = 'moge'
    result = f.validate(params)
    self.assertEqual(result, False)

  def tearDown(self):
    pass


class TimeFieldForm(forms.Form):
  csrf_protected = False
  time_field = forms.TimeField("time", required=True)

class TimeFieldTest(unittest.TestCase):
  def setUp(self):
    os.environ['REQUEST_METHOD'] = 'POST'
    local.request = Request(get_env())

  def test_validate(self):
    """TimeField validation test."""
    import datetime
    form = TimeFieldForm()
    result = form.validate({})
    self.assertEqual(result, False)
    form.reset()
    result = form.validate({'time_field': 'hoge'})
    self.assertEqual(result, False)
    form.reset()
    result = form.validate({'time_field': '10:15'})
    self.assertEqual(result, True)
    self.assertEqual(form['time_field'], datetime.time(10, 15))


class TestForm2(forms.Form):
  csrf_protected = False
  int_field = forms.IntegerField("int", min_value=5, max_value=99)
  float_field = forms.FloatField("float", min_value=5.5, max_value=99.9)
  number_field = forms.NumberField("number", min_value=5.5, max_value=99.9)

class NumberFieldTest(unittest.TestCase):
  def setUp(self):
    os.environ['REQUEST_METHOD'] = 'POST'
    local.request = Request(get_env())

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
