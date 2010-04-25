# -*- coding: utf-8 -*-

"""
Kay wrappers.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

from werkzeug.contrib.wrappers import DynamicCharsetResponseMixin
from werkzeug import Response

class DynamicCharsetResponse(DynamicCharsetResponseMixin, Response):
  pass
