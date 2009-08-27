# -*- coding: utf-8 -*-

"""
Kay authentication views.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from werkzeug import (
  unescape, redirect, Response,
)
from werkzeug.urls import (
  url_unquote_plus, url_encode,
)

from kay.utils import (
  local, render_to_response, url_for,
)
from kay.i18n import lazy_gettext as _

from forms import LoginForm

def post_session(request):
  if request.method == "GET":
    from models import TemporarySession
    temporary_session = TemporarySession.get_by_key_name(
      request.values.get("session_id"))
    if temporary_session is not None:
      temporary_session.delete()
      import datetime
      allowed_datetime = datetime.datetime.now() - \
          datetime.timedelta(seconds=10) # TODO: remove magic number
      if temporary_session.created > allowed_datetime:
        local.request.session['_user'] = temporary_session.user.key()
        return redirect(url_unquote_plus(request.values.get('next')))
  return Response("Error")
    

def login(request):
  next = url_unquote_plus(request.values.get("next"))
  owned_domain_hack = request.values.get("owned_domain_hack")
  message = ""
  form = LoginForm()
  if request.method == "POST":
    if form.validate(request.form):
      result = local.app.auth_backend.login(user_name=form.data['user_name'],
                                            password=form.data['password'])
      if result:
        if owned_domain_hack == 'True':
          original_host_url = url_unquote_plus(
            request.values.get("original_host_url"))
          url = original_host_url[:-1] + url_for("auth/post_session")
          url += '?' + url_encode({'session_id': result.key().name(),
                                   'next': next})
          return redirect(url)
        else:
          return redirect(next)
      else:
        message = _("Failed to login.")
  return render_to_response("auth/loginform.html",
                            {"form": form.as_widget(),
                             "message": message})

def logout(request):
  next = request.values.get("next")
  local.app.auth_backend.logout()
  return redirect(url_unquote_plus(next))
