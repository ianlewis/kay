# -*- coding: utf-8 -*-

"""
Views of Kay i18n app.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging

from werkzeug import (
  Response, redirect
)
from urllib import unquote_plus

from kay.utils import render_to_response
from kay.sessions.decorators import no_session
from kay.i18n import gettext as _
from kay.conf import settings

def set_language(request):
  lang = request.values['lang']
  next = unquote_plus(request.values['next'])
  ret = redirect(next)
  ret.set_cookie(settings.LANG_COOKIE_NAME, lang,
                 max_age=settings.LANG_COOKIE_AGE)
  return ret
