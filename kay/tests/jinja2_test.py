#:coding=utf-8:

from kay.utils.test import Client
from kay.utils import url_for
from kay.app import get_application
from kay.conf import LazySettings
from kay.ext.testutils.gae_test_base import GAETestBase

class Jinja2TestCase(GAETestBase):
  
  def setUp(self):
    s = LazySettings(settings_module='kay.tests.google_settings')
    self.app = get_application(settings=s)

  def test_lazy_jinja2(self):
    self.assertFalse(hasattr(self.app.app, '_jinja2_env'), "Jinja2 environment is loaded to early.")
    self.assertTrue(self.app.app.jinja2_env)
    self.assertTrue(hasattr(self.app.app, '_jinja2_env'), "Jinja2 environment is not loaded")
