# -*- coding: utf-8 -*-

"""
Kay authentication form.

:copyright: (c) 2009 by Accense Technology, Inc. See AUTHORS for more
details.
:license: BSD, see LICENSE for more details.
"""

from kay.i18n import lazy_gettext as _
from kay.utils import forms

class LoginForm(forms.Form):
  user_name = forms.TextField(required=True, label=_("user name"))
  password = forms.TextField(required=True,
                             widget=forms.PasswordInput,
                             label=_("password"))

