# -*- coding: utf-8 -*-

"""
kay.ext.gaema.views

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.

"""

from werkzeug import (
  redirect, Response
)

from kay.utils import set_cookie
from kay.utils import render_to_response
from kay.ext.gaema import (
  GoogleAuth, TwitterAuth, FacebookAuth, GAEMA_USER_KEY_FORMAT,
  NEXT_URL_KEY_FORMAT
)
from kay.ext.gaema.utils import (
  set_gaema_user, get_gaema_user
)

# Create your views here.

auth_modules = {
  'goog_openid': GoogleAuth,
  'twitter': TwitterAuth,
  'facebook': FacebookAuth,
}

def create_login_view(name):
  auth_module = auth_modules[name]
  next_url_key =  NEXT_URL_KEY_FORMAT % name
  def login_view(request, *args, **kwargs):
    def auth_callback(user):
      set_gaema_user(name, user)
    next_url = request.cookies.get(next_url_key, None)
    if next_url is None:
      next_url = "/"
    if get_gaema_user(name):
      return redirect(next_url)
    auth_instance = auth_module(request)
    if auth_instance.is_callback():
      auth_instance.get_authenticated_user(auth_callback)
      return redirect(next_url)
    auth_instance.authenticate_redirect()
  return login_view

def create_logout_view(name):
  next_url_key = NEXT_URL_KEY_FORMAT % name
  def logout_view(request, *args, **kwargs):
    set_gaema_user(name, None)
    next_url = request.cookies.get(next_url_key, None)
    if next_url is None:
      next_url = "/"
    return redirect(next_url)
  return logout_view

goog_openid_login = create_login_view("goog_openid")
twitter_login = create_login_view("twitter")
facebook_login = create_login_view("facebook")

goog_openid_logout = create_logout_view("goog_openid")
twitter_logout = create_logout_view("twitter")
facebook_logout = create_logout_view("facebook")
