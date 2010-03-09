"""
compile_css/compile_media jinja2 extesions.

:Copyright: (c) 2010 HANAI Tohru <tohru@reedom.com> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import copy
import logging
import types
import os
import re
import yaml

from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.utils import Markup
from jinja2.exceptions import TemplateAssertionError, TemplateSyntaxError

import kay
from kay.conf import settings
from kay.utils import local

from kay.ext.media_compressor import media_compiler

class CompileMediaExtension(Extension):
  # a set of names that trigger the extension.
  tags = set(['compiled_css', 'compiled_js'])

  def __init__(self, environment):
    super(CompileMediaExtension, self).__init__(environment)

    # add the defaults to the environment
    environment.extend(
    )

  def parse(self, parser):
    # get lineno at where the `compile' tag is written in the template
    token = parser.stream.next()
    lineno = token.lineno

    label = parser.parse_expression().value
    if token.value == 'compiled_css':
      node = self.get_compiled_css_urls(label)
    else:
      node = self.get_compiled_js_urls(label)
    node.set_lineno(lineno)

    return [node]

  def get_compiled_js_urls(self, label):
    t = '<script type="text/javascript" src="%s"></script>\n'

    media_compiler.set_verbose_method(media_compiler.VERBOSE_LOGGING)
    markup = ''
    for url in media_compiler.get_js_urls(label, auto_compile=False):
      markup += t.replace('%s', url)
    return nodes.Const(markup)

  def get_compiled_css_urls(self, label):
    t = '<link type="text/css" rel="stylesheet" href="%s" />\n'

    media_compiler.set_verbose_method(media_compiler.VERBOSE_LOGGING)
    markup = ''
    for url in media_compiler.get_css_urls(label, auto_compile=False):
      markup += t.replace('%s', url)
    return nodes.Const(markup)

# nicer import name
compress = CompileMediaExtension
