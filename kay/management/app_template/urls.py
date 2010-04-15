# -*- coding: utf-8 -*-
# %app_name%.urls

from kay.view_group import (
  ViewGroup, URL
)

view_groups = [
  ViewGroup(URL('/', endpoint='index', view='%app_name%.views.index'))
]
