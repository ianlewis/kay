# -*- coding: utf-8 -*-

"""
A sample of kay settings.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

DEFAULT_TIMEZONE = 'Asia/Tokyo'
DEBUG = True
PROFILE = False
SECRET_KEY = 'ReplaceItWithSecretString'
SESSION_PREFIX = 'gaesess:'
COOKIE_AGE = 1209600 # 2 weeks
COOKIE_NAME = 'KAY_SESSION'

ADD_APP_PREFIX_TO_KIND = True

ADMINS = (
)

TEMPLATE_DIRS = (
)

USE_I18N = False
DEFAULT_LANG = 'en'

INSTALLED_APPS = (
)

APP_MOUNT_POINTS = {
}

MIDDLEWARE_CLASSES = (
)
AUTH_USER_BACKEND = 'kay.auth.backends.googleaccount.GoogleBackend'
AUTH_USER_MODEL = 'kay.auth.models.GoogleUser'
