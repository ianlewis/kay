# -*- coding: utf-8 -*-

"""
kay.handlers.mail

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging

from google.appengine.api import mail
from werkzeug import Response

from kay.handlers import BaseHandler

class MailBaseHandler(BaseHandler):
  """A baseclass for Inbound mail handlers.
  """

  def __init__(self):
    import kay.sessions
    super(MailBaseHandler, self).__init__()
    setattr(self, kay.sessions.NO_SESSION, True)

  def post(self, address):
    """Transforms body to email request."""
    self.receive(mail.InboundEmailMessage(self.request.data), address)
    return Response("OK")

  def receive(self, mail_message, address):
    """Receive an email message.

    Override this method to implement an email receiver.

    Args:
      mail_message: InboundEmailMessage instance representing received
        email.
    """
    pass
