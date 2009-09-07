#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Kay wxadmin main window.

:Copyright: (c) 2009 Takashi Matsuo <tmatsuo@candit.jp> All rights reserved.
:license: BSD, see LICENSE for more details.
"""

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

  def start(self):
    thread.start_new_thread(self.run, ())

  def ask_username(self, msg):
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

  def run(self):
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

    self.Bind(wx.EVT_MENU, self.on_quit, id=ID_QUIT)
    self.Bind(wx.EVT_MENU, self.on_deploy, id=ID_DEPLOY)

    menubar.Append(file, '&File')
    self.SetMenuBar(menubar)

    self.deploy = wx.Button(self, -1, 'Deploy', (50,50))
    self.Bind(wx.EVT_BUTTON, self.on_deploy, self.deploy)

    self.Centre()
    self.Show(True)

  def on_deploy(self, event):

    from wx import xrc
    res = xrc.XmlResource(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'dialog_frame.xrc'))

    self.dialog_frame = res.LoadFrame(None, 'dialog_frame')
    self.out = xrc.XRCCTRL(self.dialog_frame, 'log_text')
    self.dialog_frame.close = xrc.XRCCTRL(self.dialog_frame, 'ok_button')
    self.dialog_frame.SetTitle('Deploying')
    self.dialog_frame.Bind(wx.EVT_BUTTON, self.on_ok,
                           self.dialog_frame.close)
    self.dialog_frame.close.Enable(False)
    self.deploy.Enable(False)
    self.dialog_frame.Show()

    self.Bind(EVT_THREAD_END, self.on_thread_end)
    self.Bind(EVT_MESSAGE_UPDATE, self.on_msg_update)
    self.Bind(EVT_ASK_PASSWORD, self.on_ask_password)
    t = AppCfgThread(self)
    t.start()

  def on_ask_password(self, event):
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

  def on_msg_update(self, event):
    self.out.AppendText(event.message)

  def on_thread_end(self, event):
    self.dialog_frame.close.Enable(True)
    self.dialog_frame.close.SetFocus()

  def on_ok(self, event):
    self.dialog_frame.Close()
    self.dialog_frame = None
    self.deploy.Enable(True)

  def on_quit(self, event):
    self.Close()

  def __del__(self):
    if self.dialog_frame is not None:
      self.dialog_frame.Close()
