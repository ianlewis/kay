# -*- coding: utf-8 -*-

"""
Kay authentication form.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from kay.i18n import lazy_gettext as _
from kay.utils import forms
from kay.utils.validators import ValidationError


class LoginForm(forms.Form):
  user_name = forms.TextField(required=True, label=_("user name"))
  password = forms.TextField(required=True, widget=forms.PasswordInput,
                             label=_("password"))


class ChangePasswordForm(forms.Form):
  old_password = forms.TextField(required=True, label=_("Old password"),
                                 max_length=32, widget=forms.PasswordInput)
  new_password = forms.TextField(required=True, label=_("New password"),
                                 max_length=32, widget=forms.PasswordInput)
  password_confirm = forms.TextField(required=True,
                                     label=_("Confirm password"),
                                     max_length=32, widget=forms.PasswordInput)

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
      
