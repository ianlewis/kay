# -*- coding: utf-8 -*-

"""
Kay authentication views.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from werkzeug import (
  unescape, redirect, Response,
)

from kay.utils import (
  local, render_to_response
)
from kay.i18n import lazy_gettext as _

from forms import LoginForm

def login(request):
  next = request.values.get("next")
  message = ""
  form = LoginForm()
  if request.method == "POST":
    if form.validate(request.form):
      if local.app.auth_backend.login(user_name=form.data['user_name'],
                                      password=form.data['password']):
        import urllib2
        return redirect(urllib2.unquote(next))
      else:
        message = _("Failed to login.")
  return render_to_response("auth/loginform.html",
                            {"form": form.as_widget(),
                             "message": message})

def logout(request):
  next = request.values.get("next")
  local.app.auth_backend.logout()
  import urllib2
  return redirect(urllib2.unquote(next))
