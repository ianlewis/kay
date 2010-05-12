# -*- coding: utf-8 -*-

"""
kay.ext.gaema.views

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.

"""

from werkzeug import redirect
from urllib import unquote_plus

from kay.conf import settings
from kay.utils import set_cookie
from kay.utils import render_to_response
from kay.ext.gaema import (
  GoogleMarketPlaceAuth, GAEMA_USER_KEY_FORMAT, NEXT_URL_KEY_FORMAT
)
from kay.ext.gaema.utils import (
  set_gaema_user, get_gaema_user, create_gaema_login_url
)
from kay.ext.gaema.services import (
  get_service_verbose_name, get_auth_module, use_hybrid,
  GOOG_OPENID, GOOG_HYBRID, TWITTER, FACEBOOK, YAHOO
)

# Create your views here.

def select_service(request, targets):
  targets = targets.split('|')
  next_url = unquote_plus(request.args.get('next_url'))
  urls = []
  for target in targets:
    verbose_name = 'Sign in with %s' % get_service_verbose_name(target)
    url = create_gaema_login_url(target, next_url)
    urls.append((target, verbose_name, url))
  if len(targets) == 1:
    return redirect(url)
  return render_to_response('gaema/select_service.html',
                            {'urls': urls})

def login(request, service):
  auth_module = get_auth_module(service)
  next_url_key = NEXT_URL_KEY_FORMAT % service
  def auth_callback(user):
    set_gaema_user(service, user)
  next_url = request.cookies.get(next_url_key, "/")
  if get_gaema_user(service):
    return redirect(next_url)
  auth_instance = auth_module(request)
  if auth_instance.is_callback():
    auth_instance.get_authenticated_user(auth_callback)
    return redirect(next_url)
  if use_hybrid(service):
    oauth_scope = getattr(settings, 'GAEMA_OAUTH_SCOPE', None)
    auth_instance.authorize_redirect(oauth_scope)
  else:
    auth_instance.authenticate_redirect()

def logout(request, service):
  next_url_key = NEXT_URL_KEY_FORMAT % service
  set_gaema_user(service, None)
  next_url = request.cookies.get(next_url_key, "/")
  return redirect(next_url)


def marketplace_login(request, domain):
  next_url_key = NEXT_URL_KEY_FORMAT % domain
  def auth_callback(user):
    set_gaema_user(domain, user)
  next_url = request.cookies.get(next_url_key, "/")
  if get_gaema_user(domain):
    return redirect(next_url)
  auth_instance = GoogleMarketPlaceAuth(request, domain)
  if auth_instance.is_callback():
    auth_instance.get_authenticated_user(auth_callback)
    return redirect(next_url)
  oauth_scope = getattr(settings, 'GAEMA_OAUTH_SCOPE', None)
  auth_instance.authorize_redirect(oauth_scope)


def marketplace_logout(request, domain):
  next_url_key = NEXT_URL_KEY_FORMAT % domain
  set_gaema_user(domain, None)
  next_url = request.cookies.get(next_url_key, "/")
  return redirect(next_url)
  
