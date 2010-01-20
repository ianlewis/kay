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
from werkzeug.utils import import_string
from werkzeug.exceptions import Forbidden

from kay.utils import (
  local, render_to_response, url_for,
)
from kay.utils import flash
from kay.i18n import lazy_gettext as _
from kay.i18n import gettext
from kay.cache.decorators import no_cache
from kay.cache import NoCacheMixin
from kay.handlers import BaseHandler
from kay.conf import settings

from kay.auth.forms import (
  LoginForm, ChangePasswordForm, ResetPasswordRequestForm, ResetPasswordForm,
)
from kay.auth.models import TemporarySession

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

@no_cache
def reset_password(request, session_key):
  form = ResetPasswordForm()
  if request.method == 'GET':
    try:
      temporary_session = TemporarySession.get(session_key)
    except Exception:
      # BadKeyError ... etc
      temporary_session = None
    if temporary_session is None:
      return Forbidden("Temporary Session might be expired.")
    # TODO: acquire new temporary session
    new_session = TemporarySession.get_new_session(temporary_session.user)
    temporary_session.delete()
    form.data['temp_session'] = str(new_session.key())
  elif request.method == 'POST' and form.validate(request.form):
    new_session = TemporarySession.get(form['temp_session'])
    user = new_session.user
    user.set_password(form['new_password'])
    new_session.delete()
    return render_to_response("auth/reset_password_success.html")
  return render_to_response("auth/reset_password.html",
                            {"form": form.as_widget()})

@no_cache
def request_reset_password(request):
  form = ResetPasswordRequestForm()
  message = ""
  if request.method == 'POST' and form.validate(request.form):
    try:
      auth_model_class = import_string(settings.AUTH_USER_MODEL)
    except (ImportError, AttributeError), e:
      raise ImproperlyConfigured, \
          'Failed to import %s: "%s".' % (settings.AUTH_USER_MODEL, e)
    user = auth_model_class.get_by_user_name(form['user_name'])
    if user is None:
      return render_to_response("auth/no_such_user.html",
                                {"user_name": form["user_name"]})
    else:
      temporary_session = TemporarySession.get_new_session(
        user, additional_tq_url='_internal/send_reset_password_instruction',
        tq_kwargs={"user_key": user.key()}
      )
      return render_to_response("auth/reset_password_finish.html")
  return render_to_response("auth/request_reset_password.html",
                            {"message": message,
                             "form": form.as_widget()})

class ChangePasswordHandler(BaseHandler, NoCacheMixin):

  def __init__(self, template_name='auth/change_password.html'):
    self.template_name = template_name

  def prepare(self):
    # TODO: check if FlashMiddleware is used.
    if not self.request.user.is_authenticated():
      raise Forbidden(_("You must sign in for this operation."))
    self.form = ChangePasswordForm()

  def get(self):
    message = flash.get_flash()
    return render_to_response(self.template_name,
                              {"form": self.form.as_widget(),
                               "message": message})

  def post(self):
    if self.form.validate(self.request.form):
      self.request.user.set_password(self.form['new_password'])
      flash.set_flash(gettext("Password changed successfully."))
      return redirect(url_for('auth/change_password'))
    return self.get()
