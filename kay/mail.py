# -*- coding: utf-8 -*-

"""
Tools for sending email.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from google.appengine.api import mail

from kay.conf import settings

def mail_admins(subject, message, fail_silently=False):
  """Sends a message to the admins, as defined by the ADMINS setting."""
  if not settings.ADMINS:
    return

  if settings.NOTIFY_ERRORS_TO_GAE_ADMINS:
    mail.send_mail_to_admins(sender=settings.ADMINS[0][1],
                             subject=subject,
                             body=message)
    return

  for admin in settings.ADMINS:
    mail.send_mail(sender=admin[1],
                   to=admin[1],
                   subject=subject,
                   body=message)
