# -*- coding: utf-8 -*-

"""
Kay context processors.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from kay.utils import url_for, reverse, create_login_url, create_logout_url
from kay.conf import settings

def request(request):
  return {"request": request}

def url_functions(request):
  return {'url_for': url_for,
          'reverse': reverse,
          'create_login_url': create_login_url,
          'create_logout_url': create_logout_url}

def media_url(request):
  import sys
  frame = sys._getframe(1)
  # ugly, but works
  while frame.f_globals['__name__'] == 'kay.utils':
    frame = frame.f_back
  app_name = frame.f_globals['__name__'].split('.')[-2]
  return {'media_url': settings.MEDIA_URL,
          'app_media_url': '%s/%s' % (settings.MEDIA_URL, app_name),
          'internal_media_url': settings.INTERNAL_MEDIA_URL}

