# -*- coding: utf-8 -*-

"""
Kay utilities.

:copyright: (c) 2009 by Kay Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import re
from jinja2 import (
  environmentfilter, Markup, escape,
)

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@environmentfilter
def nl2br(environment, value):
  result = u'<br/>'.join(u'%s' % p.replace('\n', '<br>\n')
                        for p in _paragraph_re.split(escape(value)))
  if environment.autoescape:
    result = Markup(result)
  return result
