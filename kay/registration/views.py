# -*- coding: utf-8 -*-

"""
Kay authentication views.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from werkzeug import (
  unescape, redirect, Response,
)

from kay.i18n import lazy_gettext as _
from kay.cache import NoCacheMixin
from kay.cache.decorators import no_cache
from kay.handlers import BaseHandler
from kay.utils import (
  render_to_response, url_for
)
from kay.conf import settings

from kay.registration.forms import RegistrationForm
from kay.registration.models import RegistrationProfile

class ActivateHandler(BaseHandler, NoCacheMixin):

  def __init__(self, template_name='registration/activate.html',
               extra_context=None):
    self.template_name = template_name
    self.extra_context = extra_context or {}


  def get(self, activation_key):
    account = RegistrationProfile.activate_user(activation_key)
    context = {'account': account,
               'expiration_duration': settings.ACCOUNT_ACTIVATION_DURATION}
    for key, value in self.extra_context.items():
      context[key] = callable(value) and value() or value
    return render_to_response(self.template_name, context)


class RegisterHandler(BaseHandler, NoCacheMixin):

  def __init__(self, next_url=None, form_cls=None,
               template_name='registration/registration_form.html',
               extra_context=None):
    self.next_url = next_url or url_for('registration/registration_complete')
    self.form_cls = form_cls or RegistrationForm
    self.template_name = template_name
    self.extra_context = extra_context or {}
    self.form = self.form_cls()

  def get(self):
    c = {'form': self.form.as_widget()}
    c.update(self.extra_context)
    return render_to_response(self.template_name, c)

  def post(self):
    if self.form.validate(self.request.form):
      self.form.save()
      return redirect(self.next_url)
    else:
      return self.get()

@no_cache
def registration_complete(request):
  return render_to_response('registration/registration_complete.html')
