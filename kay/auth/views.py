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
  local, render_to_response, url_for,
)
from kay.i18n import lazy_gettext as _

from forms import LoginForm

def post_session(request):
  if request.method == "GET":
    from models import TemporarySession
    import urllib2
    s = TemporarySession.get_by_key_name(request.values.get("session_id"))
    if s is not None:
      local.request.session['_user'] = s.user
      s.delete()
      return redirect(urllib2.unquote(request.values.get('next')))
  return Response("Error")
    

def login(request):
  import urllib2
  next = urllib2.unquote(request.values.get("next"))
  owned_domain_hack = request.values.get("owned_domain_hack")
  message = ""
  form = LoginForm()
  if request.method == "POST":
    if form.validate(request.form):
      result = local.app.auth_backend.login(user_name=form.data['user_name'],
                                            password=form.data['password'])
      if result:
        if owned_domain_hack == 'True':
          original_host_url = urllib2.unquote(
            request.values.get("original_host_url"))
          url = original_host_url[:-1] + url_for("auth/post_session")
          url += '?session_id=' + result.key().name() + '&next='+ \
              urllib2.quote(next, safe='')
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
  import urllib2
  return redirect(urllib2.unquote(next))
