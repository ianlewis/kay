# -*- coding: utf-8 -*-

"""
A decorators related authentication.

:Copyright: (c) 2009 Accense Technology, Inc.,
                     Ian Lewis <IanMLewis@gmail.com>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from functools import update_wrapper

from google.appengine.api import users
from werkzeug import redirect
from werkzeug.exceptions import Forbidden

from kay.utils import (
  create_login_url, create_logout_url
)

def login_required(func):
  def inner(request, *args, **kwargs):
    if request.user.is_anonymous():
      if request.is_xhr:
        return Forbidden()
      else:
        return redirect(create_login_url(request.url))
    return func(request, *args, **kwargs)
  update_wrapper(inner, func)
  return inner

def admin_required(func):
  def inner(request, *args, **kwargs):
    if not request.user.is_admin:
      if request.user.is_anonymous():
        return redirect(create_login_url(request.url))
      else:
        # TODO: Lead to more user friendly error page.
        raise Forbidden(
          description = 
          '<p>You don\'t have the permission to access the requested resource.'
          ' It is either read-protected or not readable by the server.</p>'
          ' Maybe you want <a href="%s">logout</a>?' %
          create_logout_url(request.url)
        )
    return func(request, *args, **kwargs)
  update_wrapper(inner, func)
  return inner

