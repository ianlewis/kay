# -*- coding: utf-8 -*-
from functools import update_wrapper

from werkzeug import redirect

from kay.utils import create_login_url

def login_required(func):
  def inner(request, *args, **kwargs):
    if request.user.is_anonymous():
      return redirect(create_login_url(request))
    return func(request, *args, **kwargs)
  update_wrapper(inner, func)
  return inner
