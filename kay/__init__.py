# -*- coding: utf-8 -*-
"""
Kay

This is a web framework for GAE/Python.

Requirements:
* WerkZeug
* Jinja2
* pytz
* babel
* simplejson

"""
import os
import sys

KAY_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(KAY_DIR)
LIB_DIR = os.path.join(KAY_DIR, 'lib')

def setup():
  if not PROJECT_DIR in sys.path:
    sys.path = [PROJECT_DIR] + sys.path
  if not LIB_DIR in sys.path:
    sys.path = [LIB_DIR] + sys.path
