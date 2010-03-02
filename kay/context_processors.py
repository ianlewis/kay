# -*- coding: utf-8 -*-

"""
Kay context processors.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from kay.utils import url_for, reverse, create_login_url, create_logout_url
from kay.conf import settings

def request(request):
  return {"request": request}

def url_functions(request):
  ret = {'url_for': url_for,
         'reverse': reverse,
         'create_login_url': create_login_url,
         'create_logout_url': create_logout_url}
  if settings.USE_I18N:
    from kay.i18n import create_lang_url
    ret.update({'create_lang_url': create_lang_url})
  return ret
    
def i18n(request):
    #TODO: Add available languages like django's context processor
    return {
        "language_code": request.lang,
    }

def media_url(request):
  return {'media_url': settings.MEDIA_URL,
          'internal_media_url': settings.INTERNAL_MEDIA_URL}
