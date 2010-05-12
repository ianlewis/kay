# -*- coding: utf-8 -*-

"""
kay.ext.gaema.views

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.

"""

from kay import exceptions
from kay.ext.gaema import (
  GoogleAuth, TwitterAuth, FacebookAuth, YahooAuth
)
from kay.ext.gaema.auth import OpenIdMixin

GOOG_OPENID = 'goog_openid'
GOOG_HYBRID = 'goog_hybrid'
TWITTER = 'twitter'
FACEBOOK = 'facebook'
YAHOO = 'yahoo'

available_services = [
  GOOG_OPENID,
  GOOG_HYBRID,
  TWITTER,
  FACEBOOK,
  YAHOO,
]

hybrid_services = [
  GOOG_HYBRID,
]

auth_modules = {
  GOOG_OPENID: GoogleAuth,
  GOOG_HYBRID: GoogleAuth,
  TWITTER: TwitterAuth,
  FACEBOOK: FacebookAuth,
  YAHOO: YahooAuth,
}

verbose_names = {
  GOOG_OPENID: u'Google OpenID',
  GOOG_HYBRID: u'Google OpenID(Hybrid)',
  TWITTER: u'Twitter',
  FACEBOOK: u'Facebook',
  YAHOO: u'Yahoo OpenID',
}

def get_key_name(user):
  service = user['_service']
  if service in [GOOG_OPENID, GOOG_HYBRID, YAHOO]:
    return "%s:%s" % (service, user['claimed_id'])
  if service in [TWITTER]:
    return "%s:%s" % (service, user['id'])
  if service in [FACEBOOK]:
    return "%s:%s" % (service, user['uid'])
  auth_module = get_auth_module(service)
  if issubclass(auth_module, OpenIdMixin):
    return "%s:%s" % (service, user['claimed_id'])
  raise RuntimeError('Cannot create key_name')

def use_hybrid(service_name):
  return service_name in hybrid_services

def get_auth_module(service_name):
  return auth_modules[service_name]

def get_service_verbose_name(service_name):
  return verbose_names[service_name]

def register_gaema_service(key, auth_module, verbose_name, use_hybrid=False):
  global available_services, auth_modules, verbose_names, hybrid_services
  if key in available_services:
    raise exceptions.ImproperlyConfigured(
      'Service "%s" is already registered.' % key)
  if "." in key:
    raise exceptions.ImproperlyConfigured(
      'The service_name "%s" contains ".", which is not allowed.' % key)
  if ":" in key:
    raise exceptions.ImproperlyConfigured(
      'The service_name "%s" contains ":", which is not allowed.' % key)
  available_services.append(key)
  auth_modules[key] = auth_module
  verbose_names[key] = verbose_name
  if use_hybrid:
    hybrid_services.append(key)
