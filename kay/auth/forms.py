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
  
