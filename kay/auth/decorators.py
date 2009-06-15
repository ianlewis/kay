# -*- coding: utf-8 -*-

"""
A decorators related authentication.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from functools import update_wrapper

from google.appengine.api import users
from werkzeug import redirect

from kay.utils import create_login_url

def login_required(func):
  def inner(request, *args, **kwargs):
    if request.user.is_anonymous():
      return redirect(create_login_url(request))
    return func(request, *args, **kwargs)
  update_wrapper(inner, func)
  return inner

def admin_required(func):
  def inner(request, *args, **kwargs):
    if not users.is_current_user_admin():
      # TODO: The user could be logged in already,
      # which means the login page might redirect back
      # and cause redirect loops. 
      # Need to allow redirecting to an error page.
      return redirect(create_login_url(request))
    return func(request, *args, **kwargs)
  update_wrapper(inner, func)
  return inner
