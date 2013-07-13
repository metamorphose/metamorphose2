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

import utils
import wx

[wxID_PANEL, wxID_PANELBROWSE, wxID_PANELLOGENCLOSE, wxID_PANELLOGFEXTENSION,
    wxID_PANELLOGLOCATION, wxID_PANELLOGSEPARATOR, wxID_PANELSTATICTEXT1,
    wxID_PANELSTATICTEXT2, wxID_PANELSTATICTEXT3, wxID_PANELSTATICTEXT4,
    wxID_PANELSTATICTEXT5,
] = [wx.NewId() for __init_ctrls in range(11)]

class Panel(wx.Panel):
    """Logging preferences panel."""
    def __init_itemsizer_items(self, parent):
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.staticText5, 0, border=5, flag=wx.ALL)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.staticText1, 0, border=5, flag=wx.ALL)
        #parent.AddSizer(self.dirBrowse, 0, border=3, flag=wx.BOTTOM|wx.RIGHT|wx.EXPAND)
        parent.AddWindow(self.logLocation, 0, border=10,
                         flag=wx.ALIGN_CENTER | wx.RIGHT | wx.LEFT | wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.logOptionsSizer, 0, border=20,
                        flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT)
        parent.AddSpacer(wx.Size(5, 5), border=0, flag=0)

    def __init_logoptions_sizer(self, parent):
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
        self.logOptionsSizer = wx.FlexGridSizer(cols=2, hgap=0, rows=1, vgap=3)
        self.__init_logoptions_sizer(self.logOptionsSizer)
        self.itemSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.__init_itemsizer_items(self.itemSizer)
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.AddSizer(self.itemSizer, 1, border=10,
                                flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.EXPAND)
        self.SetSizer(self.mainSizer)

    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_PANEL, name=u'Logging', parent=prnt,
                          style=wx.TAB_TRAVERSAL)
              
        self.staticText1 = wx.StaticText(id=wxID_PANELSTATICTEXT1,
                                         label=_(u'Folder to keep log files in:'), name='staticText1',
                                         parent=self)

        self.logLocation = wx.DirPickerCtrl(self, -1,
                                            style=wx.DIRP_USE_TEXTCTRL | wx.DIRP_DIR_MUST_EXIST, name=u'logLocation',
                                            size=wx.Size(275, -1))

        self.staticText2 = wx.StaticText(id=wxID_PANELSTATICTEXT2,
                                         label=_(u'Separate values with:'), name='staticText2',
                                         parent=self)

        self.logSeparator = wx.TextCtrl(id=wxID_PANELLOGSEPARATOR,
                                        name=u'logSeparator', parent=self, size=wx.Size(50, -1),
                                        value=u':::')

        self.staticText3 = wx.StaticText(id=wxID_PANELSTATICTEXT3,
                                         label=_(u'Enclose values in:'), name='staticText3', parent=self)

        self.logEnclose = wx.TextCtrl(id=wxID_PANELLOGENCLOSE,
                                      name=u'logEnclose', parent=self, size=wx.Size(50, -1), value=u'')

        self.staticText4 = wx.StaticText(id=wxID_PANELSTATICTEXT4,
                                         label=_(u'File extension:'), name='staticText4', parent=self)

        self.logFextension = wx.TextCtrl(id=wxID_PANELLOGFEXTENSION,
                                         name=u'logFextension', parent=self, size=wx.Size(50, -1),
                                         value=u'log')

        self.staticText5 = wx.StaticText(id=wxID_PANELSTATICTEXT5,
                                         label=_(u'These settings apply to loading and saving of log files.'),
                                         name='staticText5', parent=self)

        self.__init_sizers()

    def __init__(self, parent):
        self.__init_ctrls(parent)
        self.SetSizerAndFit(self.mainSizer)
        if self.logLocation.GetPath() == '':
            self.logLocation.SetPath(utils.get_user_path('undo'))

    #def init_enabled(self):
    #    self.__allow_log_options(1)

    def __allow_log_options(self, event):
        if self.alwaysMakeLog.GetValue():
            allow = True
        else:
            allow = False
        for i in (self.staticText1, self.logLocation, self.browse, self.staticText2,
                  self.staticText3, self.staticText4, self.logEnclose,
                  self.logSeparator, self.logFextension):
            i.Enable(allow)
