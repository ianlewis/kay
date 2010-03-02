# -*- coding: utf-8 -*-

"""
Kay authentication form.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import logging

from kay.i18n import lazy_gettext as _
from kay.utils import forms
from kay.utils.validators import ValidationError


class LoginForm(forms.Form):
  user_name = forms.TextField(required=True, label=_("user name"))
  password = forms.TextField(required=True, widget=forms.PasswordInput,
                             label=_("password"))


class NotifyUsernameForm(forms.Form):
  mail_address = forms.EmailField(required=True, label=_("email address"))


class ResetPasswordRequestForm(forms.Form):
  user_name = forms.TextField(required=True, label=_("user name"))


class ChangePasswordMixin(forms.Form):
  old_password = forms.TextField(required=True, label=_("Old password"),
                                 max_length=32, widget=forms.PasswordInput)

class ResetPasswordMixin(forms.Form):
  new_password = forms.TextField(required=True, label=_("New password"),
                                 max_length=32, widget=forms.PasswordInput)
  password_confirm = forms.TextField(required=True,
                                     label=_("Confirm password"),
                                     max_length=32, widget=forms.PasswordInput)
  def context_validate(self, data):
    if data['new_password'] != data['password_confirm']:
      raise ValidationError(_(u"The new passwords don't match."))
  

class ResetPasswordForm(ResetPasswordMixin):
  temp_session = forms.TextField(required=True, widget=forms.HiddenInput)

  def validate_temp_session(self, value):
    from kay.auth.models import TemporarySession
    try:
      session = TemporarySession.get(value)
      user = session.user
    except Exception, e:
      logging.warn(e)
      raise ValidationError(_(u"Invalid temporary session."))
    

class ChangePasswordForm(ChangePasswordMixin, ResetPasswordMixin):

  def validate_old_password(self, value):
    from kay.utils import local
    try:
      if not local.request.user.check_password(value):
        raise
    except Exception:
      raise ValidationError(_(u"Can not validate old password."))
      
  def context_validate(self, data):
    if data['new_password'] != data['password_confirm']:
      raise ValidationError(_(u"The new passwords don't match."))
    if data['new_password'] == data['old_password']:
      raise ValidationError(_(
          u"The new password must differ from the old one."))
