#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compile media
~~~~~~~~~~~~~

Compile media files(JavaScript/css)

:Copyright: (c) 2009 reedom, All rights reserved.
:license: BSD, see LICENSE for more details.

This file originally derives from django-compress project.
"""
import kay
kay.setup_syspath()

from kay.management.utils import (
  print_status, get_user_apps,
)
from kay.conf import settings

import kay.ext.media_compressor.default_settings as media_conf
from kay.ext.media_compressor import media_compiler

#--------------------------------------------------------------

def do_compile_media(force=("f", False)):
  '''Compile media files(JavaScript/css)
  '''
  media_compiler.set_verbose_method(media_compiler.VERBOSE_PRINT)
  media_compiler.manage_static_files()
  media_compiler.compile_css(force=force)
  media_compiler.compile_js(force=force)

