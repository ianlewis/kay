
import logging

from werkzeug import (
  BaseResponse, Request
)
from werkzeug.datastructures import Headers

from kay.utils.test import Client
from kay.app import get_application
from kay.conf import LazySettings
from kay.ext.testutils.gae_test_base import GAETestBase
from kay.utils import url_for

from kay.tests.restapp.models import RestModel

class RestJSONTestCase(GAETestBase):
  KIND_NAME_UNSWAPPED = False
  USE_PRODUCTION_STUBS = True
  CLEANUP_USED_KIND = True

  def setUp(self):
    s = LazySettings(settings_module='kay.tests.rest_settings')
    app = get_application(settings=s)
    self.client = Client(app, BaseResponse)
    self.client.test_logout()

  def tearDown(self):
    self.client.test_logout()

  def test_rest_json(self):

    headers = Headers({"Accept": "application/json"})

    response = self.client.get('/rest/metadata', headers=headers)
    self.assertEqual(response.status_code, 403)

    self.client.test_login(email="test@example.com")
    response = self.client.get('/rest/metadata', headers=headers)
    self.assertEqual(response.status_code, 403)

    self.client.test_login(email="test@example.com", is_admin="1")
    response = self.client.get('/rest/metadata', headers=headers)
    self.assertEqual(response.status_code, 200)

    self.client.test_logout()
    response = self.client.get('/rest/metadata/RestModel', headers=headers)
    self.assertEqual(response.status_code, 403)

    self.client.test_login(email="test@example.com")
    response = self.client.get('/rest/metadata/RestModel', headers=headers)
    self.assertEqual(response.status_code, 403)

    self.client.test_login(email="test@example.com", is_admin="1")
    response = self.client.get('/rest/metadata/RestModel', headers=headers)
    self.assertEqual(response.status_code, 200)


    self.client.test_logout()
    response = self.client.post(
      '/rest/RestModel',
      data='{"RestModel": {"i_prop": 12, "s_prop": "string"}}',
      content_type="application/json; charset=utf-8")
    self.assertEqual(response.status_code, 403)

    self.client.test_login(email="test@example.com")
    response = self.client.post(
      '/rest/RestModel',
      data='{"RestModel": {"i_prop": 12, "s_prop": "string"}}',
      content_type="application/json; charset=utf-8")
    self.assertEqual(response.status_code, 403)

    self.client.test_login(email="test@example.com", is_admin="1")
    response = self.client.post(
      '/rest/RestModel',
      data='{"RestModel": {"i_prop": 12, "s_prop": "string"}}',
      content_type="application/json; charset=utf-8")
    self.assertEqual(response.status_code, 200)

    key = response.data
    elm = RestModel.get(key)
    self.assertEqual(elm.s_prop, "string")
    self.assertEqual(elm.i_prop, 12)

    self.client.test_logout()
    response = self.client.post(
      '/rest/RestModel/%s' % key,
      data='{"RestModel": {"i_prop": 14}}',
      content_type="application/json; charset=utf-8")
    self.assertEqual(response.status_code, 403)

    self.client.test_login(email="test@example.com")
    response = self.client.post(
      '/rest/RestModel/%s' % key,
      data='{"RestModel": {"i_prop": 14}}',
      content_type="application/json; charset=utf-8")
    self.assertEqual(response.status_code, 403)

    self.client.test_login(email="test@example.com", is_admin="1")
    response = self.client.post(
      '/rest/RestModel/%s' % key,
      data='{"RestModel": {"i_prop": 14}}',
      content_type="application/json; charset=utf-8")
    self.assertEqual(response.status_code, 200)

    key2 = response.data
    self.assertEqual(key, key2)
    elm = RestModel.get(key)
    self.assertEqual(elm.s_prop, "string")
    self.assertEqual(elm.i_prop, 14)
    
    response = self.client.post(
      '/rest/RestModel',
      data='[{"RestModel": {"i_prop": 1, "s_prop": "foobar1"}},{"RestModel": {"i_prop": 2, "s_prop": "foobar2"}}]',
      content_type="application/json; charset=utf-8")
    self.assertEqual(response.status_code, 200)
    key3, key4 = response.data.split(',')
    elm3 = RestModel.get(key3)
    elm4 = RestModel.get(key4)
    self.assertEqual(elm3.s_prop, "foobar1")
    self.assertEqual(elm3.i_prop, 1)
    self.assertEqual(elm4.s_prop, "foobar2")
    self.assertEqual(elm4.i_prop, 2)

    response = self.client.get('/rest/RestModel', headers=headers)
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/rest/RestModel/%s' % key, headers=headers)
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/rest/RestModel/%s/s_prop' % key,
                               headers=headers)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, "string")

    response = self.client.get('/rest/RestModel/%s/i_prop' % key,
                               headers=headers)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, "14")

    self.client.test_logout()
    response = self.client.delete('/rest/RestModel/%s' % key,
                                  headers=headers)
    self.assertEqual(response.status_code, 403)

    self.client.test_login(email="test@example.com")
    response = self.client.delete('/rest/RestModel/%s' % key,
                                  headers=headers)
    self.assertEqual(response.status_code, 403)

    self.client.test_login(email="test@example.com", is_admin="1")
    response = self.client.delete('/rest/RestModel/%s' % key,
                                  headers=headers)
    self.assertEqual(response.status_code, 200)


    response = self.client.get('/rest/RestModel/%s' % key,
                               headers=headers)
    self.assertEqual(response.status_code, 404)


class RestTestCase(GAETestBase):
  KIND_NAME_UNSWAPPED = False
  USE_PRODUCTION_STUBS = True
  CLEANUP_USED_KIND = True
  KIND_PREFIX_IN_TEST = "t2"

  def setUp(self):
    s = LazySettings(settings_module='kay.tests.rest_settings')
    app = get_application(settings=s)
    self.client = Client(app, BaseResponse)
    self.client.test_logout()

  def tearDown(self):
    self.client.test_logout()

  def test_rest_operations(self):
    self.client.test_login(email="test@example.com", is_admin="1")
    response = self.client.get('/rest/metadata')
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/rest/metadata/RestModel')
    self.assertEqual(response.status_code, 200)

    response = self.client.post('/rest/RestModel', data='<?xml version="1.0" encoding="utf-8"?><RestModel><i_prop>12</i_prop><s_prop>string</s_prop></RestModel>')
    self.assertEqual(response.status_code, 200)
    key = response.data
    elm = RestModel.get(key)
    self.assertEqual(elm.s_prop, "string")
    self.assertEqual(elm.i_prop, 12)

    response = self.client.post(
      '/rest/RestModel/%s' % key,
      data='<?xml version="1.0" encoding="utf-8"?><RestModel><i_prop>14</i_prop></RestModel>')
    self.assertEqual(response.status_code, 200)
    key2 = response.data
    self.assertEqual(key, key2)
    elm = RestModel.get(key)
    self.assertEqual(elm.s_prop, "string")
    self.assertEqual(elm.i_prop, 14)

    response = self.client.get('/rest/RestModel')
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/rest/RestModel/%s' % key)
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/rest/RestModel/%s/s_prop' % key)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, "string")

    response = self.client.get('/rest/RestModel/%s/i_prop' % key)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, "14")

    response = self.client.delete('/rest/RestModel/%s' % key)
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/rest/RestModel/%s' % key)
    self.assertEqual(response.status_code, 404)
    
