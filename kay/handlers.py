# -*- coding: utf-8 -*-
# kay.handlers

import logging

from google.appengine.api import xmpp
from google.appengine.ext.webapp import xmpp_handlers

from werkzeug.exceptions import (
  MethodNotAllowed, NotImplemented
)

METHODS = ['GET', 'POST', 'HEAD', 'OPTIONS', 'PUT', 'DELETE', 'TRACE']

class KayHandler(object):

  def __init__(self):
    pass

  def __call__(self, request):
    self.request = request
    prepare_func = getattr(self, 'prepare', None)
    if callable(prepare_func):
      response = prepare_func()
      if response:
        return response
    if request.method in METHODS:
      func = getattr(self, request.method.lower(), None)
      if callable(func):
        try:
          return func()
        except Exception, e:
          self.handle_exception(e)
          raise
      else:
        return NotImplemented()
    else:
      return MethodNotAllowed()

  def handle_exception(self, exception):
    pass


class XMPPBaseHandler(KayHandler):
  """A baseclass for XMPP handlers.

  Implements a straightforward message delivery pattern. When a message is
  received, message_received is called with a Message object that encapsulates
  the relevant details. Users can reply using the standard XMPP API, or the
  convenient .reply() method on the Message object.
  """

  def __init__(self):
    import kay.sessions
    super(XMPPBaseHandler, self).__init__()
    setattr(self, kay.sessions.NO_SESSION, True)


  def message_received(self, message):
    """Called when a message is sent to the XMPP bot.

    Args:
      message: Message: The message that was sent by the user.
    """
    raise NotImplementedError()

  def handle_exception(self, exception):
    """Called if this handler throws an exception during execution.

    Args:
      exception: the exception that was thrown
      debug_mode: True if the web application is running in debug mode
    """
    if self.xmpp_message:
      self.xmpp_message.reply('Oops. Something went wrong.')
    super(XMPPBaseHandler, self).handle_exception(exception)

  def post(self):
    try:
      self.xmpp_message = xmpp.Message(self.request.form)
    except xmpp.InvalidMessageError, e:
      logging.error("Invalid XMPP request: Missing required field %s", e[0])
      return
    self.message_received(self.xmpp_message)


class XMPPCommandHandler(xmpp_handlers.CommandHandlerMixin, XMPPBaseHandler):
  pass
