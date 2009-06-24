# -*- coding: utf-8 -*-
"""
kay.utils.jinja2.code_loaders
~~~~~~~~~~~~~~~~~~~~~~~~~

Set of Jinja2 loaders that use pre-compiled templates stored as Python code.
It is indended to be used on Google App Engine, where bytecode cache can't
be used.

Using these loaders, templates won't be parsed at all, only compiled from
the pre-generated Python code. This eliminates the biggest Jinja2 overhead
due to App Engine limitations, and complex templates will render ten or more
times faster.

To pre-compile whole template directories, use gaefy.jinja2.compiler.

:copyright: 2009 by tipfy.org.
:license: BSD, see LICENSE.txt for more details.
"""

import base64
import logging

from jinja2.loaders import FileSystemLoader, PackageLoader, DictLoader, \
  FunctionLoader, PrefixLoader, ChoiceLoader

try:
  code_cache
except NameError:
  logging.debug("Initializing code_cache.")
  code_cache = {}

def set_code(name, code):
  code_cache[base64.b64encode(name)] = code


def get_code_by_name(name):
  encoded = base64.b64encode(name)
  if encoded in code_cache:
    return code_cache[encoded]
  return None


class BaseCodeLoader(object):
  """Base mixin class for loaders that use pre-parsed Jinja2 templates stored
  as Python code.
  """
  def load(self, environment, name, globals=None):
    """Loads a pre-parsed template, stored as Python code."""
    if globals is None:
      globals = {}
    code = get_code_by_name(name)
    if code is not None:
      logging.debug("Loaded the code from module global variable.")
    else:
      logging.debug("Load the templates from precompiled source.")
      source, filename, uptodate = self.get_source(environment, name)
      code = compile(source, filename, 'exec')
      set_code(name, code)
    return environment.template_class.from_code(environment, code, globals)


class FileSystemCodeLoader(BaseCodeLoader, FileSystemLoader):
  pass


class PackageCodeLoader(BaseCodeLoader, PackageLoader):
  pass


class DictCodeLoader(BaseCodeLoader, DictLoader):
  pass


class FunctionCodeLoader(BaseCodeLoader, FunctionLoader):
  pass


class PrefixCodeLoader(BaseCodeLoader, PrefixLoader):
  pass


class ChoiceCodeLoader(BaseCodeLoader, ChoiceLoader):
  pass
