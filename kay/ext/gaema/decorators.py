# -*- coding: utf-8 -*-

"""
kay.ext.gaema.decorators

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp>
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging
from functools import update_wrapper

from werkzeug import redirect

from kay.ext.gaema.utils import (
  get_gaema_user, create_gaema_login_url
)
from kay.utils.decorators import auto_adapt_to_methods

def create_inner_func_for_auth(name, func):
  def inner(request, *args, **kwargs):
    if get_gaema_user(name):
      return func(request, *args, **kwargs)
    else:
      return redirect(create_gaema_login_url(name, request.url))
  return inner

def goog_openid_login_required(func):
  inner = create_inner_func_for_auth("goog_openid", func)
  update_wrapper(inner, func)
  return inner

def twitter_login_required(func):
  inner = create_inner_func_for_auth("twitter", func)
  update_wrapper(inner, func)
  return inner

def facebook_login_required(func):
  inner = create_inner_func_for_auth("facebook", func)
  update_wrapper(inner, func)
  return inner

def gaema_login_required(name):
  def outer(func):
    inner = create_inner_func_for_auth(name, func)
    update_wrapper(inner, func)
    return inner
  return outer

goog_openid_login_required = auto_adapt_to_methods(goog_openid_login_required)
twitter_login_required = auto_adapt_to_methods(twitter_login_required)
facebook_login_required = auto_adapt_to_methods(facebook_login_required)
