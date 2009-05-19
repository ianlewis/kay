# -*- coding: utf-8 -*-
"""
Tools for sending email.
TODO: use local.app.app_settings.ADMINS instead of kay.conf.settings
"""

from google.appengine.api import mail

from kay.conf import settings

def mail_admins(subject, message, fail_silently=False):
  """Sends a message to the admins, as defined by the ADMINS setting."""
  if not settings.ADMINS:
    return
  for admin in settings.ADMINS:
    mail.send_mail(sender=admin[1],
                   to=admin[1],
                   subject=subject,
                   body=message)
