# -*- coding: utf-8 -*-
"""
    gaema.httpclient
    ~~~~~~~~~~~~~~~~

    HTTP client to support `tornado.auth` on Google App Engine.

    :copyright: 2010 by tipfy.org.
    :license: Apache License Version 2.0. See LICENSE.txt for more details.
"""
import functools
import logging

from google.appengine.api import urlfetch


class HttpResponseError(object):
    """A dummy response used when urlfetch raises an exception."""
    code = 404
    body = '404 Not Found'
    error = 'Error 404'


class AsyncHTTPClient(object):
    """An non-blocking HTTP client that uses `google.appengine.api.urlfetch`."""
    def fetch(self, url, callback, **kwargs):
        # Replace kwarg keys.
        kwargs['payload'] = kwargs.pop('body', None)
        kwargs['deadline'] = 10
        try:
          result = urlfetch.fetch(url, **kwargs)
          code = result.status_code
          setattr(result, 'body', result.content)
          if code < 200 or code >= 300:
            logging.debug(result.body)
            setattr(result, 'error', 'Error %d' % code)
          else:
            setattr(result, 'error', None)
            logging.debug(result.body)
        except urlfetch.DownloadError, e:
          logging.debug(e)
          result = HttpResponseError()
        args = () + (result,)
        return callback(*args)
