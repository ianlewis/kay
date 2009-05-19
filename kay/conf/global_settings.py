# -*- coding: utf-8 -*-
import os

DEFAULT_TIMEZONE = 'Asia/Tokyo'
DEBUG = True
PROFILE = False
SECRET_KEY = 'please set secret keys here'
SESSION_PREFIX = 'gaesess:'
COOKIE_AGE = 1209600 # 2 weeks
COOKIE_NAME = 'KAY_SID'

ADMINS = (
  ['Admin', 'admin@example.com'],
)

TEMPLATE_DIRS = (
)

USE_I18N = True
DEFAULT_LANG = 'en'

INSTALLED_APPS = (
)

MIDDLEWARE_CLASSES = (
  'kay.sessions.middleware.SessionMiddleware',
  'kay.auth.middleware.GoogleAuthenticationMiddleware',
)
