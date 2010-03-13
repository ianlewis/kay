# -*- coding:utf-8 -*-

"""
:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp>,
                     Atsushi Odagiri <aodagx@gmail.com>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.

http://groups.google.com/group/json-rpc/web/json-rpc-2-0

errors:
code 	message 	meaning
-32700 	Parse error 	Invalid JSON was received by the server.
An error occurred on the server while parsing the JSON text.
-32600 	Invalid Request 	The JSON sent is not a valid Request object.
-32601 	Method not found 	The method does not exist / is not available.
-32602 	Invalid params 	Invalid method parameter(s).
-32603 	Internal error 	Internal JSON-RPC error.
-32099 to -32000 	Server error 	Reserved for implementation-defined server-errors.

"""

PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603
errors = {}
errors[PARSE_ERROR] = "Parse Error"
errors[INVALID_REQUEST] = "Invalid Request"
errors[METHOD_NOT_FOUND] = "Method Not Found"
errors[INVALID_PARAMS] = "Invalid Params"
errors[INTERNAL_ERROR] = "Internal Error"

try:
  import json
except ImportError:
  try:
    import django.utils.simplejson as json
  except ImportError:
    import simplejson as json

import sys
import logging
import itertools

from werkzeug import Request, Response
from werkzeug import exceptions

class JsonRpcApplication(object):
  def __init__(self, methods=None):
    if methods is not None:
      self.methods = methods
    else:
      self.methods = {}

  def add_module(self, mod, namespace=None):
    if namespace is None:
      namespace = mod.__name__
    for k, v in ((k, v) for k, v in mod.__dict__.iteritems() 
                 if not k.startswith('_') and callable(v)):
      self.add(namespace + '.' + k, v)

  def add(self, name, func):
    self.methods[name] = func

  def process(self, data):
    if data.get('jsonrpc') != "2.0":
      return {'jsonrpc':'2.0',
              'id':data.get('id'),
              'error':{'code':INVALID_REQUEST,
                       'message':errors[INVALID_REQUEST]}}
    if 'method' not in data:
      return {'jsonrpc':'2.0',
              'id':data.get('id'),
              'error':{'code':INVALID_REQUEST,
                       'message':errors[INVALID_REQUEST]}}
      
    methodname = data['method']
    if not isinstance(methodname, basestring):
      return {'jsonrpc':'2.0',
              'id':data.get('id'),
              'error':{'code':INVALID_REQUEST,
                       'message':errors[INVALID_REQUEST]}}
      
    if methodname.startswith('_'):
      return {'jsonrpc':'2.0',
              'id':data.get('id'),
              'error':{'code':METHOD_NOT_FOUND,
                       'message':errors[METHOD_NOT_FOUND]}}


    if methodname not in self.methods:
      return {'jsonrpc':'2.0',
              'id':data.get('id'),
              'error':{'code':METHOD_NOT_FOUND,
                       'message':errors[METHOD_NOT_FOUND]}}


    method = self.methods[methodname]
    try:
      params = data.get('params', [])
      if isinstance(params, list):
        result = method(*params)
      elif isinstance(params, dict):
        result = method(**dict([(str(k), v) for k, v in params.iteritems()]))
      else:
        return {'jsonrpc':'2.0',
                'id':data.get('id'),
                'error':{'code':INVALID_REQUEST,
                         'message':errors[INVALID_REQUEST]}}
      resdata = None
      if data.get('id'):

        resdata = {
          'jsonrpc':'2.0',
          'id':data.get('id'),
          'result':result,
        }
      return resdata
    except Exception, e:
      return {'jsonrpc':'2.0',
              'id':data.get('id'),
              'error':{'code':INTERNAL_ERROR,
                       'message':errors[INTERNAL_ERROR],
                       'data':str(e)}}


  def __call__(self, environ, start_response):
    request = Request(environ)
    if request.method != "POST":
      raise exceptions.MethodNotAllowed

    if not request.content_type.startswith('application/json'):
      raise exceptions.BadRequest
    try:
      data = json.loads(request.data)
    except ValueError, e:
      resdata = {'jsonrpc':'2.0',
                 'id':None,
                 'error':{'code':PARSE_ERROR,
                          'message':errors[PARSE_ERROR]}}

    else:
      if isinstance(data, dict):
        resdata = self.process(data)
      elif isinstance(data, list):
        if len([x for x in data if not isinstance(x, dict)]):
          resdata = {'jsonrpc':'2.0',
                     'id':None,
                     'error':{'code':INVALID_REQUEST,
                              'message':errors[INVALID_REQUEST]}}
        else:
          resdata = [d for d in (self.process(d) for d in data) 
                     if d is not None]
            

    response = Response(content_type="application/json")

    if resdata:
      response.headers["Cache-Control"] = "no-cache"
      response.headers["Pragma"] = "no-cache"
      response.headers["Expires"] = "-1"
      response.data = json.dumps(resdata)
    return response(environ, start_response)


def getmod(modname):
  try:
    __import__(modname)
  except ImportError, e:
    logging.warn("import failed: %s." % e)
    return None
  mod = sys.modules[modname]
  return mod


def HTTPExceptionMiddleware(app):
  def wrap(environ, start_response):
    try:
      return app(environ, start_response)
    except exceptions.HTTPException, e:
      return e(environ, start_response)
  return wrap

def make_application(methods):
  app = JsonRpcApplication()
  for name, value in methods.iteritems():
    if ":" in value:
      modname, funcname = value.split(":", 1)
      mod = getmod(modname)
      if mod:
        app.add(name, getattr(mod, funcname))
    else:
      modname = value
      mod = getmod(modname)
      if mod:
        app.add_module(mod, name)
  app = HTTPExceptionMiddleware(app)
  return app

