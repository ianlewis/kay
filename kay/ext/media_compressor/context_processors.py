# -*- coding: utf-8 -*-

"""
kay.ext.media_compressor.context_processors

:Copyright: (c) 2010 Takashi MATSUO <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from jinja2 import Markup

from kay.ext.media_compressor import media_compiler


def get_compiled_js_urls(label):
  t = '<script type="text/javascript" src="%s"></script>\n'

  media_compiler.set_verbose_method(media_compiler.VERBOSE_LOGGING)
  markup = ''
  for url in media_compiler.get_js_urls(label, auto_compile=False):
    markup += t.replace('%s', url)
  return Markup(markup)

def get_compiled_css_urls(label):
  t = '<link type="text/css" rel="stylesheet" href="%s" />\n'

  media_compiler.set_verbose_method(media_compiler.VERBOSE_LOGGING)
  markup = ''
  for url in media_compiler.get_css_urls(label, auto_compile=False):
    markup += t.replace('%s', url)
  return Markup(markup)


def media_urls(request):
  return {'compiled_js': get_compiled_js_urls,
          'compiled_css': get_compiled_css_urls}
