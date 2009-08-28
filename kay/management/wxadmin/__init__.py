
import wx

from mainframe import MainFrame

def do_wxadmin():
  app = wx.App()
  MainFrame(None, -1, 'Kay WxAdmin')
  app.MainLoop()

