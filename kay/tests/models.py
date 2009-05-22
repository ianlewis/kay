# -*- coding: utf-8 -*-

"""
Models for Kay tests.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from google.appengine.ext import db

class TestModel(db.Model):
  number = db.IntegerProperty()
  data = db.StringProperty()
  is_active = db.BooleanProperty()
