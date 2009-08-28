#!/usr/bin/python

# submenu.py

import os
import logging

try:
  import wx
  import wx.lib.dialogs
except:
  pass


ID_QUIT = 1
ID_DEPLOY = 2
ID_DEPLOY_BUTTON = 2

class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(350, 250))

        self.dialog_frame = None
        self.process = None
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.Bind(wx.EVT_END_PROCESS, self.OnProcessEnded)

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

    def OnProcessEnded(self, evt):
        stream = self.process.GetInputStream()

        if stream.CanRead():
            text = stream.read()
            self.out.AppendText(text)

        stream = self.process.GetErrorStream()

        if stream.CanRead():
            text = stream.read()
            self.out.AppendText(text)

        self.process.Destroy()
        self.process = None
        self.dialog_frame.close.Enable(True)

    def OnIdle(self, evt):
        if self.process is not None:
            stream = self.process.GetInputStream()

            if stream.CanRead():
                text = stream.read()
                self.out.AppendText(text)

            stream = self.process.GetErrorStream()

            if stream.CanRead():
                text = stream.read()
                self.out.AppendText(text)

    def OnDeploy(self, event):
        self.dialog_frame = wx.Frame(None, -1, 'Deploying', size=(500,500),
                                     style=wx.CAPTION|wx.RESIZE_BORDER)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.out = wx.TextCtrl(self.dialog_frame, -1, style=wx.TE_MULTILINE)
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
        self.process = wx.Process(self)
        self.process.Redirect();
        cmd = '/usr/bin/python manage.py appcfg update'
        pid = wx.Execute(cmd, wx.EXEC_ASYNC, self.process)


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
