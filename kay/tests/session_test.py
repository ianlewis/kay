
from werkzeug import (
  BaseResponse, Client, Request
)

from kay.app import get_application
from kay.conf import LazySettings
from kay.ext.testutils.gae_test_base import GAETestBase

class SessionMiddlewareTestCase(GAETestBase):
  KIND_NAME_UNSWAPPED = False
  USE_PRODUCTION_STUBS = True
  CLEANUP_USED_KIND = True

  def setUp(self):
    s = LazySettings(settings_module='kay.tests.settings')
    app = get_application(settings=s)
    self.client = Client(app, BaseResponse)

  def tearDown(self):
    pass

  def test_countup(self):
    response = self.client.get('/countup')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, '1')
    response = self.client.get('/countup')
    self.assertEqual(response.data, '2')
    response = self.client.get('/countup')
    self.assertEqual(response.data, '3')
    response = self.client.get('/countup')
    self.assertEqual(response.data, '4')
    response = self.client.get('/countup')
    self.assertEqual(response.data, '5')

class SessionMiddlewareWithSecureCookieTestCase(GAETestBase):
  KIND_NAME_UNSWAPPED = False
  USE_PRODUCTION_STUBS = True
  CLEANUP_USED_KIND = True

  def setUp(self):
    s = LazySettings(settings_module='kay.tests.securecookie_session_settings')
    app = get_application(settings=s)
    self.client = Client(app, BaseResponse)

  def tearDown(self):
    pass

  def test_countup(self):
    response = self.client.get('/countup')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, '1')
    response = self.client.get('/countup')
    self.assertEqual(response.data, '2')
    response = self.client.get('/countup')
    self.assertEqual(response.data, '3')
    response = self.client.get('/countup')
    self.assertEqual(response.data, '4')
    response = self.client.get('/countup')
    self.assertEqual(response.data, '5')
