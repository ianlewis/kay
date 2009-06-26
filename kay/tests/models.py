# -*- coding: utf-8 -*-

"""
Models for Kay tests.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from google.appengine.ext import db

from kay.utils.forms import ValidationError
from kay.utils.forms.modelform import ModelForm

def CreateMaxLengthValidator(length):
  def MaxLengthValidator(val):
    if len(val) > length:
      raise ValidationError("Too long")
    return True
  return MaxLengthValidator
  

class TestModel(db.Model):
  number = db.IntegerProperty(required=True)
  data_field = db.StringProperty(required=True,
                                 validator=CreateMaxLengthValidator(20))
  is_active = db.BooleanProperty(required=True)
  string_list_field = db.StringListProperty(required=True)

class TestModelForm(ModelForm):
  csrf_protected = False
  class Meta():
    model = TestModel
  def __init__(self, instance=None, initial=None):
    super(TestModelForm, self).__init__(instance, initial)
    self.string_list_field.min_size = 1
