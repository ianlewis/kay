# -*- coding: utf-8 -*-
"""
kay.utils.flash

:Copyright: (c) 2009 tipfy.org,
                Takashi Matsuo <tmatsuo@candit.jp>
                All rights reserved.
:license: BSD, see LICENSE for more details.
"""
from base64 import b64encode, b64decode
import simplejson

from kay.conf import settings
from kay.utils import local
from kay.i18n import lazy_gettext as _

def get_flash():
  """Reads and deletes a flash message. Flash messages are stored in a cookie
  and automatically deleted when read.

  :return:
      The data stored in a flash, if any.
  """
  key = settings.FLASH_COOKIE_NAME
  data = getattr(local, 'flash_message', None)
  if data is None:
    if key in local.request.cookies:
      data = local.request.cookies[key]
  local.flash_message = None
  if data:
    return simplejson.loads(b64decode(data))
  return u''


def set_flash(data):
  """Sets a flash message. Flash messages are stored in a cookie
  and automatically deleted when read.

  :param data:
    Flash data to be serialized and stored as JSON.
  :return:
    ``None``.
  """
  local.flash_message = b64encode(simplejson.dumps(data))


class FlashMiddleware(object):
  def process_response(self, request, response):
    key = settings.FLASH_COOKIE_NAME
    data = getattr(local, 'flash_message', None)
    try:
      if data:
        response.set_cookie(key, value=data)
      else:
        response.delete_cookie(key)
    except Exception:
      pass
    return response
