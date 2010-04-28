# -*- coding: utf-8 -*-

"""
kay.ext.gaema is a bit modified version of gaema.
Original gaema is hosted at http://code.google.com/p/gaema/
"""

import functools
import logging
import base64

from werkzeug.routing import RequestRedirect

from kay.ext.gaema import auth
from kay.utils import set_cookie
from kay.conf import settings

mount_point = "/_ah/gaema"

GAEMA_USER_KEY_FORMAT = "_%s_user"
NEXT_URL_KEY_FORMAT = "_nexturl_%s"


class RequestAdapter(object):
  """Adapter to transform a `webob` request into a request with the
  attributes expected by `tornado.auth`.

  It must define at least the following attributes or functions:

  request.arguments: a dictionary of GET parameters mapping to a list
  of values.
  request.host: current request host.
  request.path: current request path.
  request.full_url(): a function returning the current full URL.
  """
  def __init__(self, request):
    """Initializes the request adapter.

    :param request:
    A `werkzeug.Request` instance.
    """
    self.arguments = {}
    for k, v in request.args.items():
      self.arguments.setdefault(k, []).append(v)

    self.full_url = lambda: request.url
    self.host = request.host
    self.path = request.path

class HttpException(Exception):
  pass

class GAEMultiAuthMixin(object):

  arg_in_callback = None

  def __init__(self, request):
    self.request = RequestAdapter(request)
    self._request = request
    self.settings = settings.GAEMA_SETTINGS
    self.redirect_to = None

  def is_callback(self):
    return self._request.args.get(self.arg_in_callback, None) is not None

  def require_setting(self, name, feature=None):
    if not self.settings.has_key(name):
      if feature is None:
        feature = name
      raise Exception("You must define `%s` key in your GAEMA_SETTINGS"
                      " settings variable in your"
                      " application to use %s." % (name, feature))

  def async_callback(self, callback, *args, **kwargs):
    if callback is None:
      return None

    if args or kwargs:
      callback = functools.partial(callback, *args, **kwargs)

    def wrapper(*args, **kwargs):
      try:
        return callback(*args, **kwargs)
      except RequestRedirect:
        raise
      except Exception, e:
        logging.error('Exception during callback', exc_info=True)

    return wrapper

  def redirect(self, url):
    raise RequestRedirect(url)

  _ARG_DEFAULT = []
  def get_argument(self, name, default=_ARG_DEFAULT, strip=True):
    value = self._request.args.get(name, default)
    if value is self._ARG_DEFAULT:
      raise HttpException('Missing request argument %s' % name)

    if strip:
      value = value.strip()

    return value

  def get_cookie(self, name, default=None):
    cookie = self._request.cookies.get(name, None)
    if cookie is None:
      return default
    return str(base64.b64decode(cookie))

  def set_cookie(self, name, value, domain=None, expires=None, path='/',
                 expires_days=None):
    if expires_days is not None and not expires:
      expires = datetime.datetime.utcnow() + datetime.timedelta(
        days=expires_days)
    value = str(base64.b64encode(value))

    set_cookie(name, value, path=path, domain=domain, expires=expires)


class GoogleAuth(GAEMultiAuthMixin, auth.GoogleMixin):
  arg_in_callback = 'openid.mode'


class TwitterAuth(GAEMultiAuthMixin, auth.TwitterMixin):
  arg_in_callback = 'oauth_token'


class FacebookAuth(GAEMultiAuthMixin, auth.FacebookMixin):
  arg_in_callback = 'session'


class YahooAuth(GAEMultiAuthMixin, auth.YahooMixin):
  arg_in_callback = 'openid.mode'
