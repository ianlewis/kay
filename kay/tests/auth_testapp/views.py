# -*- coding: utf-8 -*-

"""
Kay datastore auth test views.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from werkzeug import (
  unescape, redirect, Response,
)

from kay.utils import (
  local, render_to_response, url_for,
)
from kay.auth.decorators import login_required

def index(request):
  return Response("OK")

@login_required
def secret(request):
  return Response("secret")
