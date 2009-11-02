# -*- coding: utf-8 -*-

"""
Kay registration form.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from werkzeug.utils import import_string

from kay.i18n import lazy_gettext as _
from kay.utils import forms
from kay.utils.validators import ValidationError
from kay.conf import settings

class RegistrationForm(forms.Form):
  user_name = forms.TextField(required=True, label=_(u"user name"),
                              max_length=30)
  email = forms.EmailField(required=True, label=_(u"email address"))
  password = forms.TextField(required=True, widget=forms.PasswordInput,
                             label=_("password"))
  password_confirm = forms.TextField(required=True, widget=forms.PasswordInput,
                                     label=_("password(again)"))

  def validate_user_name(self, value):
    user_classname = settings.AUTH_USER_MODEL
    user_cls = import_string(user_classname)
    user = user_cls.get_by_key_name(user_cls.get_key_name(value))
    if user:
      raise ValidationError(_(u"This user name is already taken."
                              " Please choose another user name."))
    
  def context_validate(self, data):
    if data['password'] != data['password_confirm']:
      raise ValidationError(_(u"The passwords don't match."))

  def save(self):
    user_classname = settings.AUTH_USER_MODEL
    user_cls = import_string(user_classname)
    user = user_cls.create_inactive_user(self['user_name'], self['password'],
                                         self['email'])
    return user
