#!/usr/bin/python

# submenu.py

import os
import logging
import thread
import time

import wx
import wx.lib.dialogs
import wx.lib.newevent

from kay.management.utils import print_status

ID_QUIT = 1
ID_DEPLOY = 2
ID_DEPLOY_BUTTON = 2

(ThreadEndEvent, EVT_THREAD_END) = wx.lib.newevent.NewEvent()
(MsgUpdateEvent, EVT_MESSAGE_UPDATE) = wx.lib.newevent.NewEvent()
(AskPassEvent, EVT_ASK_PASSWORD) = wx.lib.newevent.NewEvent()

class RedirectText:
  def __init__(self, win):
    self.win = win

  def write(self, string):
    evt = MsgUpdateEvent(message=string)
    wx.PostEvent(self.win, evt)

  def flush(self, *args, **kwargs):
    pass

class AppCfgThread(object):

  def __init__(self, win):
    self.win = win

  def Start(self):
    thread.start_new_thread(self.Run, ())

  def ask_username(self, msg):
    print_status("ask_username")
    evt = AskPassEvent(message=msg)
    wx.PostEvent(self.win, evt)
    while 1:
      if (self.win.username is not None) and (self.win.password is not None):
        ret = self.win.username
        self.win.username = None
        if ret == '' or self.win.password == '':
          evt = AskPassEvent(message=msg)
          wx.PostEvent(self.win, evt)
        else:
          return ret
      else:
        time.sleep(0.1)

  def ask_pass(self, msg):
    print_status("ask_pass")
    if self.win.password:
      ret = self.win.password
      self.win.password = None
      return ret
    evt = AskPassEvent(message=msg)
    wx.PostEvent(self.win, evt)
    while 1:
      if self.win.password is not None:
        ret = self.win.password
        self.win.password = None
        if ret == '':
          evt = AskPassEvent(message=msg)
          wx.PostEvent(self.win, evt)
        else:
          return ret
      else:
        time.sleep(0.1)

  def Run(self):
    from google.appengine.tools import appcfg
    from kay.management.preparse import do_preparse_apps
    import sys
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    redir = RedirectText(self.win)
    sys.stdout = redir
    sys.stderr = redir

    import time
    do_preparse_apps()
    args = ['manage.py', 'update', os.getcwdu()]

    try:
      app = appcfg.AppCfgApp(args, raw_input_fn=self.ask_username,
                             password_input_fn=self.ask_pass, error_fh=redir)
      result = app.Run()
      if result:
        print_status('Failed Deploying application.')
      else:
        from kay.conf import settings
        if settings.PROFILE and 'update' in sys.argv:
          print_status('--------------------------\n' \
                         'WARNING: PROFILER ENABLED!\n' \
                         '--------------------------')
    except KeyboardInterrupt:
      print_status('Interrupted.')
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evt = ThreadEndEvent()
    wx.PostEvent(self.win, evt)

class AskPassDialog(wx.Dialog):
  def __init__(self, parent, id, title, username='', password='',
               **kwargs):
    wx.Dialog.__init__(self, parent, id, title, **kwargs)
    sizer = wx.BoxSizer(wx.VERTICAL)

    box = wx.BoxSizer(wx.HORIZONTAL)

    label = wx.StaticText(self, -1, "Email/Username:", size=(120,-1))
    box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    self.username = wx.TextCtrl(self, -1, username, size=(180,-1))
    box.Add(self.username, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

    sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    box = wx.BoxSizer(wx.HORIZONTAL)

    label = wx.StaticText(self, -1, "Password:", size=(120,-1))
    box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    self.password = wx.TextCtrl(self, -1, "", size=(180,-1),
                                style=wx.TE_PASSWORD)
    box.Add(self.password, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
    sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
    sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

    btnsizer = wx.StdDialogButtonSizer()
        
        
    btn = wx.Button(self, wx.ID_OK)
    btn.SetHelpText("The OK button completes the dialog")
    btn.SetDefault()
    btnsizer.AddButton(btn)

    btnsizer.Realize()

    sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    self.SetSizer(sizer)
    sizer.Fit(self)
    self.Centre()


class MainFrame(wx.Frame):
  def __init__(self, parent, id, title):
    wx.Frame.__init__(self, parent, id, title, size=(350, 250))

    self.dialog_frame = None
    self.username = None
    self.password = None
    self.past_username = None

    menubar = wx.MenuBar()

    file = wx.Menu()
    deploy = file.Append(ID_DEPLOY, '&Deploy')
    file.AppendSeparator()

    quit = wx.MenuItem(file, ID_QUIT, '&Quit\tCtrl+W')
    file.Append(ID_QUIT, '&Quit')

    self.Bind(wx.EVT_MENU, self.OnQuit, id=ID_QUIT)
    self.Bind(wx.EVT_MENU, self.OnDeploy, id=ID_DEPLOY)

    menubar.Append(file, '&File')
    self.SetMenuBar(menubar)

    self.deploy = wx.Button(self, -1, "Deploy", (50,50))
    self.Bind(wx.EVT_BUTTON, self.OnDeploy, self.deploy)

    self.Centre()
    self.Show(True)

  def OnDeploy(self, event):
    self.dialog_frame = wx.Frame(None, -1, 'Deploying', size=(500,500),
                                 style=wx.CAPTION|wx.RESIZE_BORDER)
    vbox = wx.BoxSizer(wx.VERTICAL)
    self.out = wx.TextCtrl(self.dialog_frame, -1,
                           style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2)
    self.dialog_frame.close = wx.Button(self.dialog_frame, -1, "OK",
                                        (50,50))
    vbox.Add(self.out, 1, wx.EXPAND|wx.ALL)
    vbox.Add(self.dialog_frame.close, 0, wx.BOTTOM)
    self.dialog_frame.SetSizer(vbox)
    self.dialog_frame.Bind(wx.EVT_BUTTON, self.OnOK,
                           self.dialog_frame.close)

    self.dialog_frame.close.Enable(False)
    self.deploy.Enable(False)

    self.dialog_frame.Center()
    self.dialog_frame.Show()
    self.Bind(EVT_THREAD_END, self.OnThreadEnd)
    self.Bind(EVT_MESSAGE_UPDATE, self.OnMsgUpdate)
    self.Bind(EVT_ASK_PASSWORD, self.OnAskPassword)
    t = AppCfgThread(self)
    t.Start()

  def OnAskPassword(self, event):
    if self.username is not None and self.password is not None:
      return
    dlg = AskPassDialog(self, -1, 'Input your email/username and password',
                        username=self.past_username or '',
                        password='',
                        style=wx.DEFAULT_DIALOG_STYLE & ~wx.CLOSE_BOX)

    if dlg.ShowModal() == wx.ID_OK:
      self.past_username = self.username = dlg.username.GetValue()
      self.password = dlg.password.GetValue()
    else:
      self.username = ''
      self.password = ''
    dlg.Destroy()

  def OnMsgUpdate(self, event):
    self.out.AppendText(event.message)

  def OnThreadEnd(self, event):  
    self.dialog_frame.close.Enable(True)
    self.dialog_frame.close.SetFocus()

  def OnOK(self, event):
    self.dialog_frame.Close()
    self.dialog_frame = None
    self.deploy.Enable(True)

  def OnQuit(self, event):
    self.Close()

  def __del__(self):
    if self.dialog_frame is not None:
      self.dialog_frame.Close()
    if self.process is not None:
      self.process.Detach()
      self.process.CloseOutput()
      self.process = None
