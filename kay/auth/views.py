# -*- coding: utf-8 -*-

"""
Kay authentication views.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from urllib import unquote_plus

from werkzeug import (
  unescape, redirect, Response,
)
from werkzeug.urls import url_encode

from kay.utils import (
  local, render_to_response, url_for,
)
from kay.i18n import lazy_gettext as _
from kay.cache.decorators import no_cache
from kay.cache import NoCacheMixin
from kay.handlers import BaseHandler

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
          datetime.timedelta(seconds=10)
      if temporary_session.created > allowed_datetime:
        from kay.sessions import renew_session
        renew_session(request)
        request.session['_user'] = temporary_session.user.key()
        return redirect(unquote_plus(request.values.get('next')))
  return Response("Error")

@no_cache
def login(request):
  from kay.auth import login

  next = unquote_plus(request.values.get("next"))
  owned_domain_hack = request.values.get("owned_domain_hack")
  message = ""
  form = LoginForm()
  if request.method == "POST":
    if form.validate(request.form):
      result = login(request, user_name=form.data['user_name'],
                              password=form.data['password'])
      if result:
        if owned_domain_hack == 'True':
          original_host_url = unquote_plus(
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

@no_cache
def logout(request):
  from kay.auth import logout

  logout(request)
  next = request.values.get("next")
  return redirect(unquote_plus(next))


class ChangePasswordHandler(BaseHandler, NoCacheMixin):

  def __init__(self, template_name='auth/change_password.html'):
    self.template_name = template_name
