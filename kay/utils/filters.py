# -*- coding: utf-8 -*-

"""
Kay utilities.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
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
