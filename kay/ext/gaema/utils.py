# -*- coding: utf-8 -*-

"""
kay.ext.gaema.utils

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from werkzeug.contrib.securecookie import SecureCookie
from werkzeug.exceptions import InternalServerError

from kay.utils import (
  set_cookie, url_for, local
)
from kay.conf import settings
from kay.ext.gaema import (
  NEXT_URL_KEY_FORMAT, GAEMA_USER_KEY_FORMAT
)

from kay.ext.gaema import services

def get_valid_services():
  return getattr(settings, 'GAEMA_VALID_SERVICES', [services.GOOG_OPENID])

def create_gaema_login_url(service, nexturl="/"):
  next_url_key = NEXT_URL_KEY_FORMAT % service
  set_cookie(next_url_key, nexturl)
  return url_for("gaema/login", service=service)

def create_marketplace_login_url(domain, nexturl="/"):
  next_url_key = NEXT_URL_KEY_FORMAT % domain
  set_cookie(next_url_key, nexturl)
  return url_for("gaema/marketplace_login", domain=domain)

def create_gaema_logout_url(service, nexturl="/"):
  next_url_key = NEXT_URL_KEY_FORMAT % service
  set_cookie(next_url_key, nexturl)
  return url_for("gaema/logout", service=service)

def create_marketplace_logout_url(domain, nexturl="/"):
  next_url_key = NEXT_URL_KEY_FORMAT % domain
  set_cookie(next_url_key, nexturl)
  return url_for("gaema/marketplace_logout", domain=domain)

def get_gaema_user(service):
  try:
    gaema_user_key = GAEMA_USER_KEY_FORMAT % service
    if hasattr(settings, "GAEMA_STORAGE") and \
          settings.GAEMA_STORAGE == "cookie":
      user_data = local.request.cookies.get(gaema_user_key, None)
      if user_data:
        return SecureCookie.unserialize(user_data,
                                        secret_key=settings.SECRET_KEY)
    else:
      return local.request.session.get(gaema_user_key, None)
  except Exception, e:
    raise InternalServerError('Getting gaema_user failed, reason: %s' % e)

def set_gaema_user(service, user):
  gaema_user_key = GAEMA_USER_KEY_FORMAT % service
  if hasattr(settings, "GAEMA_STORAGE") and settings.GAEMA_STORAGE == "cookie":
    secure_cookie = SecureCookie(user, secret_key=settings.SECRET_KEY)
    user_data = secure_cookie.serialize()
    set_cookie(gaema_user_key, user_data)
  else:
    from kay.sessions import renew_session
    renew_session(local.request)
    local.request.session[gaema_user_key] = user
    local.request.session.modified = True
  
