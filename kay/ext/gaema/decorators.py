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
from werkzeug.urls import url_quote_plus

from kay.utils import url_for
from kay.utils.decorators import auto_adapt_to_methods
from kay.ext.gaema.utils import (
  get_gaema_user, create_gaema_login_url, create_marketplace_login_url,
  get_valid_services
)
from kay.ext.gaema.services import (
  GOOG_OPENID, GOOG_HYBRID, TWITTER, FACEBOOK,
)

def create_inner_func_for_auth(func, *targets):
  def inner(request, *args, **kwargs):
    for service in targets:
      if get_gaema_user(service):
        return func(request, *args, **kwargs)
    return redirect(url_for('gaema/select_service', targets='|'.join(targets),
                            next_url=url_quote_plus(request.url)))
  return inner

def gaema_login_required(*services):
  def outer(func):
    inner = create_inner_func_for_auth(func, *services)
    update_wrapper(inner, func)
    return inner
  return auto_adapt_to_methods(outer)

def marketplace_login_required(func):
  def inner(request, *args, **kwargs):
    if get_gaema_user(kwargs['domain_name']):
      return func(request, *args, **kwargs)
    return redirect(create_marketplace_login_url(kwargs['domain_name'],
                                                 nexturl=request.url))
  return inner

marketplace_login_required = auto_adapt_to_methods(marketplace_login_required)
