# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2015 ianaré sévi <ianare@gmail.com>
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

[wxID_PANEL, wxID_PANELITEMCOUNTFORPROGDIALOG, wxID_PANELRENREFRESHMIN,
    wxID_PANELSHOWPREVIEWHIGHLIGHT, wxID_PANELSHOWPREVIEWICONS,
    wxID_PANELSHOWPROGRESSDIALOG, wxID_PANELSTATICTEXT1, wxID_PANELSTATICTEXT2,
    wxID_PANELSTATICTEXT3, wxID_PANELONLYSHOWCHANGEDITEMS
 ] = [wx.NewId() for __init_ctrls in range(10)]


class Panel(wx.Panel):
    def __init_itemsizer_items(self, parent):
        parent.AddWindow(self.showPreviewIcons, 0, border=10, flag=wx.ALL)
        parent.AddWindow(self.onlyShowChangedItems, 0, border=10, flag=wx.ALL)
        parent.AddWindow(self.showPreviewHighlight, 0, border=10, flag=wx.ALL)
        parent.AddWindow(self.staticText2, 0, border=10, flag=wx.ALL)
        parent.AddSizer(self.boxsizer1, 0, border=25, flag=wx.LEFT)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.showProgressDialog, 0, border=10, flag=wx.ALL)
        parent.AddSizer(self.boxsizer2, 0, border=25, flag=wx.LEFT)

    def _init_boxsizer1(self, parent):
        parent.AddWindow(self.staticText1, 0, border=8,
                         flag=wx.ALIGN_CENTER | wx.RIGHT)
        parent.AddWindow(self.renRefreshMin, 0, border=0, flag=wx.ALIGN_CENTER)

    def _init_boxsizer2(self, parent):
        parent.AddWindow(self.staticText3, 0, border=10,
                         flag=wx.RIGHT | wx.ALIGN_CENTER)
        parent.AddWindow(self.itemCountForProgDialog, 0, border=0, flag=0)

    def __init_sizers(self):
        self.boxsizer1 = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.boxsizer2 = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.itemSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self._init_boxsizer1(self.boxsizer1)
        self._init_boxsizer2(self.boxsizer2)
        self.__init_itemsizer_items(self.itemSizer)
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.AddSizer(self.itemSizer, 0, border=10,
                                flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
        self.SetSizer(self.mainSizer)

    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_PANEL, name=u'Display', parent=prnt,
                          style=wx.TAB_TRAVERSAL)

        self.showPreviewIcons = wx.CheckBox(id=wxID_PANELSHOWPREVIEWICONS,
                                            label=_(u'Show thumbnails in preview'), name=u'showPreviewIcons',
                                            parent=self)
        self.showPreviewIcons.SetValue(True)

        self.onlyShowChangedItems = wx.CheckBox(id=wxID_PANELONLYSHOWCHANGEDITEMS,
                                                label=_(u'Only preview items that will change'),
                                                name=u'onlyShowChangedItems', parent=self)
        self.onlyShowChangedItems.SetValue(False)
        self.onlyShowChangedItems.Bind(wx.EVT_CHECKBOX,
                                       self.show_changed_items_checkbox,
                                       id=wxID_PANELONLYSHOWCHANGEDITEMS)

        self.showPreviewHighlight = wx.CheckBox(id=wxID_PANELSHOWPREVIEWHIGHLIGHT,
                                                label=_(u'Highlight changed items in preview'),
                                                name=u'showPreviewHighlight', parent=self)
        self.showPreviewHighlight.SetValue(True)

        self.staticText2 = wx.StaticText(id=wxID_PANELSTATICTEXT2,
                                         label=_(u"Change the refresh rate of the renaming operation:"),
                                         name='staticText2', parent=self)

        self.staticText1 = wx.StaticText(id=wxID_PANELSTATICTEXT1,
                                         label=_(u"Refresh rate maximum:"), name='staticText1',
                                         parent=self)

        self.renRefreshMin = wx.SpinCtrl(id=wxID_PANELRENREFRESHMIN, initial=80,
                                         max=300, min=1, name=u'renRefreshMin', parent=self,
                                         size=wx.Size(55, -1), style=wx.SP_ARROW_KEYS, value='80')
        self.renRefreshMin.SetValue(80)
        self.renRefreshMin.SetToolTipString(_(u"Higher = faster ; Lower = more feedback"))

        self.showProgressDialog = wx.CheckBox(id=wxID_PANELSHOWPROGRESSDIALOG,
                                              label=_(u"Show progress dialog when previewing many items"),
                                              name=u'showProgressDialog', parent=self)
        self.showProgressDialog.SetValue(True)
        self.showProgressDialog.Bind(wx.EVT_CHECKBOX,
                                     self.show_progress_dialog_checkbox,
                                     id=wxID_PANELSHOWPROGRESSDIALOG)

        self.staticText3 = wx.StaticText(id=wxID_PANELSTATICTEXT3,
                                         label=_(u"Number of items:"), name='staticText3', parent=self)

        self.itemCountForProgDialog = wx.SpinCtrl(id=wxID_PANELITEMCOUNTFORPROGDIALOG,
                                                  initial=200, max=100000, min=5, name=u'itemCountForProgDialog',
                                                  parent=self, size=wx.Size(75, -1),
                                                  style=wx.SP_ARROW_KEYS)
        self.itemCountForProgDialog.SetValue(200)
        self.__init_sizers()

    def __init__(self, parent):
        self.__init_ctrls(parent)
        self.SetSizerAndFit(self.mainSizer)

    def init_enabled(self):
        self.show_progress_dialog_checkbox(False)
        self.show_changed_items_checkbox(False)

    def show_changed_items_checkbox(self, event):
        if self.onlyShowChangedItems.GetValue():
            self.showPreviewHighlight.Enable(False)
        else:
            self.showPreviewHighlight.Enable(True)

    def show_progress_dialog_checkbox(self, event):
        if self.showProgressDialog.GetValue():
            self.itemCountForProgDialog.Enable(True)
            self.staticText3.Enable(True)
        else:
            self.itemCountForProgDialog.Enable(False)
            self.staticText3.Enable(False)
