
import sys

from kay.management.utils import print_status

def do_wxadmin():
  try:
    import wx
    from mainframe import MainFrame
  except:
    print_status('Can not import wxpython.')
    sys.exit(-1)
    
  app = wx.App()
  MainFrame(None, -1, 'Kay WxAdmin')
  app.MainLoop()

