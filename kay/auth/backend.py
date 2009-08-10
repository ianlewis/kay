# -*- coding: utf-8 -*-

"""
Kay authentication backends.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from kay.conf import settings
from kay.utils import (
  local, url_for
)
import urllib2

class DatastoreBackend(object):

  def create_login_url(self, url):
    return url_for("auth/login", next=urllib2.quote(url,safe=''))

  def create_logout_url(self, url):
    return url_for("auth/logout", next=urllib2.quote(url,safe=''))
