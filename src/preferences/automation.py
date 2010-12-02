# -*- coding: utf-8 -*-
#Boa:FramePanel:panel

# Automation preferences panel

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

[wxID_PANEL, wxID_PANELALWAYSMAKELOG, wxID_PANELAUTOSELECTALL,
 wxID_PANELPREVIEWONCONFIG, wxID_PANELRELOADAFTERRENAME,
 wxID_PANELAUTOSHOWERROR,
] = [wx.NewId() for __init_ctrls in range(6)]

class Panel(wx.Panel):
    def __init_mainsizer_items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.autoSelectAll, 0, border=10, flag=wx.ALL)
        parent.AddWindow(self.reloadAfterRename, 0, border=10, flag=wx.ALL)
        parent.AddWindow(self.previewOnConfig, 0, border=10, flag=wx.ALL)
        parent.AddWindow(self.alwaysMakeLog, 0, border=10, flag=wx.ALL)
        parent.AddWindow(self.autoShowError, 0, border=10, flag=wx.ALL)
        parent.AddSpacer(wx.Size(5, 5), border=0, flag=0)

    def __init_sizers(self):
        # generated method, don't edit
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.__init_mainsizer_items(self.mainSizer)

        self.SetSizer(self.mainSizer)

    def __init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANEL, name=u'Automation', parent=prnt,
              pos=wx.Point(921, 392), size=wx.Size(416, 335),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(416, 335))

        self.autoSelectAll = wx.CheckBox(id=wxID_PANELAUTOSELECTALL,
              label=_(u'Select all items when loading a directory'),
              name=u'autoSelectAll', parent=self, pos=wx.Point(10, 10),
              style=0)
        self.autoSelectAll.SetValue(True)

        self.reloadAfterRename = wx.CheckBox(id=wxID_PANELRELOADAFTERRENAME,
              label=_(u'Re-load directory contents after renaming'),
              name=u'reloadAfterRename', parent=self, pos=wx.Point(10, 52),
              style=0)

        self.alwaysMakeLog = wx.CheckBox(id=wxID_PANELALWAYSMAKELOG,
              label=_(u'Keep a log of all renaming operations'),
              name=u'alwaysMakeLog', parent=self, pos=wx.Point(10, 136),
              style=0)

        self.previewOnConfig = wx.CheckBox(id=wxID_PANELPREVIEWONCONFIG,
              label=_(u'Preview selection when loading a configuration'),
              name=u'previewOnConfig', parent=self, pos=wx.Point(10, 94),
              style=0)
        self.previewOnConfig.SetValue(True)

        self.autoShowError = wx.CheckBox(id=wxID_PANELAUTOSHOWERROR,
              label=_(u'Automatically show errors after preview'),
              name=u'autoShowError', parent=self, pos=wx.Point(15, 234),
              size=wx.Size(288, 22), style=0)

        self.__init_sizers()

    def __init__(self, parent):
        self.__init_ctrls(parent)
        self.SetSizerAndFit(self.mainSizer)
