# -*- coding: utf-8 -*-

from kay.auth.models import AnonymousUser

def get_user(request):
  return AnonymousUser()
