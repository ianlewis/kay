# -*- coding: utf-8 -*-

"""
A sample of kay settings.

:Copyright: (c) 2009 Accense Technology, Inc. All rights reserved.
:license: BSD, see LICENSE for more details.
"""

DEFAULT_TIMEZONE = 'Asia/Tokyo'
DEBUG = True
PROFILE = False
SECRET_KEY = 'hogehoge'
SESSION_PREFIX = 'gaesess:'
COOKIE_AGE = 1209600 # 2 weeks
COOKIE_NAME = 'KAY_SID'

ADD_APP_PREFIX_TO_KIND = True

ADMINS = (
)

TEMPLATE_DIRS = (
  'templates',
)

USE_I18N = True
DEFAULT_LANG = 'en'

INSTALLED_APPS = (
)

APP_MOUNT_POINTS = {
}

CONTEXT_PROCESSORS = (
  'kay.context_processors.request',
  'kay.context_processors.url_functions',
  'kay.context_processors.media_url',
)

MIDDLEWARE_CLASSES = (
  'kay.auth.middleware.GoogleAuthenticationMiddleware',
)
AUTH_USER_MODEL = 'kay.auth.models.GoogleUser'
