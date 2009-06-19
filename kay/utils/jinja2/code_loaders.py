# -*- coding: utf-8 -*-
"""
gaefy.jinja2.code_loaders
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

from jinja2.loaders import FileSystemLoader, PackageLoader, DictLoader, \
  FunctionLoader, PrefixLoader, ChoiceLoader

class BaseCodeLoader(object):
  """Base mixin class for loaders that use pre-parsed Jinja2 templates stored
  as Python code.
  """
  def load(self, environment, name, globals=None):
    """Loads a pre-parsed template, stored as Python code."""
    if globals is None:
      globals = {}

    # first we try to get the source for this template together
    # with the filename and the uptodate function.
    source, filename, uptodate = self.get_source(environment, name)

    # build a python code object.
    code = compile(source, filename, 'exec')

    return environment.template_class.from_code(environment, code,
                                                globals, uptodate)


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
