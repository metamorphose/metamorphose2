# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2013 ianaré sévi <ianare@gmail.com>
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
    """Automation preferences panel."""

    def __init_itemsizer_items(self, parent):
        parent.AddWindow(self.autoSelectAll, 0, border=10, flag=wx.ALL)
        parent.AddWindow(self.reloadAfterRename, 0, border=10, flag=wx.ALL)
        parent.AddWindow(self.previewOnConfig, 0, border=10, flag=wx.ALL)
        parent.AddWindow(self.alwaysMakeLog, 0, border=10, flag=wx.ALL)
        parent.AddWindow(self.autoShowError, 0, border=10, flag=wx.ALL)
        parent.AddSpacer(wx.Size(5, 5), border=0, flag=0)

    def __init_sizers(self):
        self.itemSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.__init_itemsizer_items(self.itemSizer)
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.AddSizer(self.itemSizer, 0, border=10,
                                flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
        self.SetSizer(self.mainSizer)

    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_PANEL, name=u'Automation', parent=prnt,
                          style=wx.TAB_TRAVERSAL)

        self.autoSelectAll = wx.CheckBox(id=wxID_PANELAUTOSELECTALL,
                                         label=_(u'Select all items when loading a directory'),
                                         name=u'autoSelectAll', parent=self)
        self.autoSelectAll.SetValue(True)

        self.reloadAfterRename = wx.CheckBox(id=wxID_PANELRELOADAFTERRENAME,
                                             label=_(u'Re-load directory contents after renaming'),
                                             name=u'reloadAfterRename', parent=self)

        self.alwaysMakeLog = wx.CheckBox(id=wxID_PANELALWAYSMAKELOG,
                                         label=_(u'Keep a log of all renaming operations'),
                                         name=u'alwaysMakeLog', parent=self)

        self.previewOnConfig = wx.CheckBox(id=wxID_PANELPREVIEWONCONFIG,
                                           label=_(u'Preview selection when loading a configuration'),
                                           name=u'previewOnConfig', parent=self)
        self.previewOnConfig.SetValue(True)

        self.autoShowError = wx.CheckBox(id=wxID_PANELAUTOSHOWERROR,
                                         label=_(u'Automatically show errors after preview'),
                                         name=u'autoShowError', parent=self)

        self.__init_sizers()

    def __init__(self, parent):
        self.__init_ctrls(parent)
        self.SetSizerAndFit(self.mainSizer)
