# -*- coding: utf-8 -*-

"""
Kay context processors.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from kay.utils import url_for, reverse, create_login_url, create_logout_url

def request(request):
  return {"request": request}

def url_functions(request):
  return {'url_for': url_for,
          'reverse': reverse,
          'create_login_url': create_login_url,
          'create_logout_url': create_logout_url}
