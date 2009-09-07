# -*- coding: utf-8 -*-

"""
Kay wxadmin management command.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

import sys

from kay.management.utils import print_status

def do_wxadmin():
  try:
    import wx
    from mainframe import MainFrame
  except:
    print_status('Can not import wxpython.')
    raise
    
  app = wx.App()
  MainFrame(None, -1, 'Kay WxAdmin')
  app.MainLoop()

