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

import sys, os
libdir = os.path.join(
  os.path.abspath(os.path.dirname(__file__)), "lib")
sys.path = [libdir] + sys.path
