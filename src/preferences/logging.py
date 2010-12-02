# -*- coding: utf-8 -*-
#Boa:FramePanel:panel

# Logging preferences panel

# Copyright (C) 2006-2010 ianaré sévi <ianare@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import wx
import utils

[wxID_PANEL, wxID_PANELBROWSE, wxID_PANELLOGENCLOSE, wxID_PANELLOGFEXTENSION,
 wxID_PANELLOGLOCATION, wxID_PANELLOGSEPARATOR, wxID_PANELSTATICTEXT1,
 wxID_PANELSTATICTEXT2, wxID_PANELSTATICTEXT3, wxID_PANELSTATICTEXT4,
 wxID_PANELSTATICTEXT5,
] = [wx.NewId() for __init_ctrls in range(11)]

class Panel(wx.Panel):
    def __init_mainsizer_items(self, parent):
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.staticText5, 0, border=5, flag=wx.ALL)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.staticText1, 0, border=5, flag=wx.ALL)
        parent.AddSizer(self.dirBrowse, 0, border=3, flag=wx.BOTTOM | wx.EXPAND)
        parent.AddSizer(self.logOptionsSizer, 0, border=20,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT)
        parent.AddSpacer(wx.Size(5, 5), border=0, flag=0)

    def __init_dirbrowse_items(self, parent):
        parent.AddWindow(self.logLocation, 1, border=20,
              flag=wx.ALIGN_CENTER | wx.LEFT)
        parent.AddWindow(self.browse, 0, border=5,
              flag=wx.ALIGN_CENTER | wx.ALL)

    def __init_logoptions_sizer_items(self, parent):
        parent.AddWindow(self.staticText2, 0, border=10,
              flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        parent.AddWindow(self.logSeparator, 0, border=0, flag=0)
        parent.AddWindow(self.staticText3, 0, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddWindow(self.logEnclose, 0, border=0, flag=0)
        parent.AddWindow(self.staticText4, 0, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddWindow(self.logFextension, 0, border=0, flag=0)

    def __init_sizers(self):
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.dirBrowse = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.logOptionsSizer = wx.FlexGridSizer(cols=2, hgap=0, rows=1, vgap=3)
        self.__init_mainsizer_items(self.mainSizer)
        self.__init_dirbrowse_items(self.dirBrowse)
        self.__init_logoptions_sizer_items(self.logOptionsSizer)
        self.SetSizer(self.mainSizer)

    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_PANEL, name=u'Logging', parent=prnt,
              pos=wx.Point(981, 684), size=wx.Size(416, 335),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(416, 335))

        self.staticText1 = wx.StaticText(id=wxID_PANELSTATICTEXT1,
              label=_(u'Folder to keep log files in:'), name='staticText1',
              parent=self, style=0)

        self.logLocation = wx.TextCtrl(id=wxID_PANELLOGLOCATION,
              name=u'logLocation', parent=self, size=wx.Size(275, -1),
              style=0, value=u'')

        self.browse = wx.Button(id=wxID_PANELBROWSE, label='...',
              name=u'browse', parent=self, size=wx.Size(50, -1),
              style=0)
        self.browse.Bind(wx.EVT_BUTTON, self.on_browse_button,
              id=wxID_PANELBROWSE)

        self.staticText2 = wx.StaticText(id=wxID_PANELSTATICTEXT2,
              label=_(u'Separate values with:'), name='staticText2',
              parent=self, style=0)

        self.logSeparator = wx.TextCtrl(id=wxID_PANELLOGSEPARATOR,
              name=u'logSeparator', parent=self, pos=wx.Point(179, 114),
              size=wx.Size(50, -1), style=0, value=u':::')

        self.staticText3 = wx.StaticText(id=wxID_PANELSTATICTEXT3,
              label=_(u'Enclose values in:'), name='staticText3', parent=self,
              style=0)

        self.logEnclose = wx.TextCtrl(id=wxID_PANELLOGENCLOSE,
              name=u'logEnclose', parent=self, pos=wx.Point(179, 144),
              size=wx.Size(50, -1), style=0, value=u'')

        self.staticText4 = wx.StaticText(id=wxID_PANELSTATICTEXT4,
              label=_(u'File extension:'), name='staticText4', parent=self,
              style=0)

        self.logFextension = wx.TextCtrl(id=wxID_PANELLOGFEXTENSION,
              name=u'logFextension', parent=self, size=wx.Size(50, -1),
              style=0, value=u'log')

        self.staticText5 = wx.StaticText(id=wxID_PANELSTATICTEXT5,
              label=_(u'These settings apply to loading and saving of log files.'),
              name='staticText5', parent=self, style=0)

        self.__init_sizers()

    def __init__(self, parent):
        self.__init_ctrls(parent)
        self.SetSizerAndFit(self.mainSizer)
        #self.allowLogOptions(1)
        if self.logLocation.GetValue() == '':
            self.logLocation.SetValue(utils.get_user_path('undo'))

    #def init_enabled(self):
    #    self.allowLogOptions(1)

    def allowLogOptions(self, event):
        if self.alwaysMakeLog.GetValue():
           allow = True
        else:
            allow = False
        for i in (self.staticText1,self.logLocation,self.browse,self.staticText2,
                  self.staticText3,self.staticText4,self.logEnclose,
                  self.logSeparator,self.logFextension):
            i.Enable(allow)

    def on_browse_button(self, event):
        dlg = wx.DirDialog(self,_(u"Choose a directory:"),
            style=wx.DD_DEFAULT_STYLE)
        dlg.SetPath(self.logLocation.GetValue())
        try:
            if dlg.ShowModal() == wx.ID_OK:
                dir = dlg.GetPath()
                self.logLocation.SetValue(dir)
        finally: dlg.Destroy()
