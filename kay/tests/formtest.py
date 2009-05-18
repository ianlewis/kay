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
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub
from google.appengine.api import mail_stub
from google.appengine.api import urlfetch_stub
from google.appengine.api.memcache import memcache_stub
from google.appengine.api import user_service_stub

import kay
from werkzeug import Request

from kay.utils import local
from kay.utils import forms

def _(v):
  return v

class GAETestBase(unittest.TestCase):

  def get_env(self):
    env = dict(os.environ)
    env['wsgi.input'] = sys.stdin
    env['wsgi.errors'] = sys.stderr
    env['wsgi.version'] = "1.0"
    env['wsgi.run_once'] = True
    env['wsgi.url_scheme'] = 'http'
    env['wsgi.multithread']  = False
    env['wsgi.multiprocess'] = True
    return env
    
  def setUp(self):
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    stub = datastore_file_stub.DatastoreFileStub('test','/dev/null',
                                                 '/dev/null')
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)

    apiproxy_stub_map.apiproxy.RegisterStub(
      'user', user_service_stub.UserServiceStub())

    apiproxy_stub_map.apiproxy.RegisterStub(
      'memcache', memcache_stub.MemcacheServiceStub())

class TestModel(db.Model):
  number = db.IntegerProperty()
  data = db.StringProperty()
  is_active = db.BooleanProperty()
  
class TestForm(forms.Form):
  csrf_protected = False
  username = forms.TextField(_("user name"), required=True)
  password = forms.TextField(_("password"), required=True)
  password_again = forms.TextField(_("confirm password"), required=True)
  model_field = forms.ModelField(TestModel, label=_("ModelField Test"),
                                 required=True, filter=('is_active =', True),
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
    os.environ['REQUEST_METHOD'] = 'POST'
    local.request = Request(self.get_env())
    f = TestForm()
    self.assertEqual(f.validate({'username': 'hoge'}), False)
    valid_params = {
      'username': 'hoge',
      'password': 'fugafuga',
      'password_again': 'fugafuga',
      'model_field': str(TestModel.all().get().key())
    }
    result = f.validate(valid_params)
    self.assertEqual(result, True)

  def tearDown(self):
    entries = TestModel.all().fetch(100)
    db.delete(entries)

class TestForm2(forms.Form):
  csrf_protected = False
  float_field = forms.FloatField("float", min_value=5.5, max_value=99.9)

class FloatFieldTest(GAETestBase):
  def setUp(self):
    super(FloatFieldTest, self).setUp()
    os.environ['REQUEST_METHOD'] = 'POST'
    local.request = Request(self.get_env())

  def test_validate_float(self):
    """
    Float value validation test.
    """
    f = TestForm2()
    result = f.validate({'float_field': 10.7})
    self.assertEqual(result, True)
    result = f.validate({'float_field': 'ten'})
    self.assertEqual(result, False)

  def test_min(self):
    """
    Minimal value validation test.
    """
    f = TestForm2()
    result = f.validate({'float_field': 5.4})
    self.assertEqual(result, False)

  def test_max(self):
    """
    Maximum value validation test.
    """
    f = TestForm2()
    result = f.validate({'float_field': 100.1})
    self.assertEqual(result, False)

if __name__ == "__main__":
  unittest.main()
