# -*- coding: utf-8 -*-
#
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

[wxID_PANEL, wxID_PANELCLEARUNDO, wxID_PANELENCODINGGROUP,
 wxID_PANELENCODINGSELECT, wxID_PANELSHOWHIDDENDIRS, wxID_PANELSTATICBOX1,
 wxID_PANELSTATICTEXT1, wxID_PANELSTATICTEXT2, wxID_PANELUSEDIRTREE,
] = [wx.NewId() for __init_ctrls in range(9)]

class Panel(wx.Panel):
    def __init_main_sizer(self, parent):
        parent.AddSpacer(wx.Size(8, 15), border=0, flag=0)
        parent.AddWindow(self.clearUndo, 0, border=15, flag=wx.LEFT)
        parent.AddSpacer(wx.Size(8, 15), border=0, flag=0)
        parent.AddWindow(self.useDirTree, 0, border=15, flag=wx.LEFT)
        parent.AddSpacer(wx.Size(5, 5), border=10, flag=0)
        parent.AddWindow(self.showHiddenDirs, 0, border=25, flag=wx.LEFT)
        parent.AddSpacer(wx.Size(-1, 20), border=0, flag=0)
        parent.AddSizer(self.encodingSizer, 0, border=15, flag=wx.LEFT)
        parent.AddSpacer(wx.Size(8, 35), border=0, flag=0)

    def _init_encodingsizer(self, parent):
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.staticText1, 0, border=5, flag=wx.ALL)
        parent.AddWindow(self.encodingGroup, 0, border=5, flag=wx.LEFT|wx.RIGHT)
        parent.AddSpacer(wx.Size(-1, 15), border=0, flag=wx.LEFT)
        parent.AddWindow(self.staticText2, 0, border=5, flag=wx.ALL)
        parent.AddWindow(self.encodingSelect, 0, border=5,
              flag=wx.BOTTOM | wx.LEFT|wx.RIGHT)

    def __init_sizers(self):
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.encodingSizer = wx.StaticBoxSizer(box=self.staticBox1,
              orient=wx.VERTICAL)
        self.__init_main_sizer(self.mainSizer)
        self._init_encodingsizer(self.encodingSizer)

        self.SetSizer(self.mainSizer)

    def __init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANEL, name=u'General', parent=prnt,
              style=wx.TAB_TRAVERSAL)

        self.staticBox1 = wx.StaticBox(id=wxID_PANELSTATICBOX1,
              label=_(u'Encoding used in audio tags:'), name='staticBox1',
              parent=self)

        self.clearUndo = wx.CheckBox(id=wxID_PANELCLEARUNDO,
              label=_(u'Clear out undo on start up'), name=u'clearUndo',
              parent=self)

        self.useDirTree = wx.CheckBox(id=wxID_PANELUSEDIRTREE,
              label=_(u'Use directory tree view'), name=u'useDirTree',
              parent=self)
        self.useDirTree.Bind(wx.EVT_CHECKBOX, self.dirTreeEnabled,
              id=wxID_PANELUSEDIRTREE)
        self.useDirTree.SetValue(True)

        self.showHiddenDirs = wx.CheckBox(id=wxID_PANELSHOWHIDDENDIRS,
              label=_(u'Show Hidden directories in tree view'),
              name=u'showHiddenDirs', parent=self)

        self.staticText1 = wx.StaticText(id=wxID_PANELSTATICTEXT1,
              label=_(u'Select language group:'), name='staticText1',
              parent=self)

        self.encodingGroup = wx.Choice(choices=[_(u"Use System Default"),
              _(u'All Languages / Unicode'), _(u'Western Europe'),
              _(u'Central & Eastern Europe'), _(u'Esperanto, Maltese'),
              _(u'Nordic Languages'), _(u'Celtic Languages'),
              _(u'Baltic Languages'), _(u'Cyrillic Languages'), _(u'Greek'),
              _(u'Turkish'), _(u'Hebrew'), _(u'Arabic'), _(u'Urdu'), _(u'Thai'),
              _(u'Vietnamese'), _(u'Traditional Chinese'),
              _(u'Simplified Chinese'), _(u'Unified Chinese'), _(u'Korean'),
              _(u'Japanese'), ], id=wxID_PANELENCODINGGROUP,
              name=u'encodingGroup', parent=self,
              size=wx.Size(260, -1))
        self.encodingGroup.SetSelection(0)
        self.encodingGroup.Bind(wx.EVT_CHOICE, self._set_encoding_options,
              id=wxID_PANELENCODINGGROUP)

        self.encodingSelect = wx.ComboBox(choices=[], id=wxID_PANELENCODINGSELECT,
              name=u'encodingSelect', parent=self,
              size=wx.Size(260, -1))

        self.staticText2 = wx.StaticText(id=wxID_PANELSTATICTEXT2,
              label=_(u'Select encoding:'), name='staticText2', parent=self)

        self.__init_sizers()

    def _make_encoding_select(self, choicesList):
        self.encodingSelect = wx.ComboBox(choices=choicesList,
              id=wxID_PANELENCODINGSELECT, name=u'encodingSelect', parent=self,
              style=wx.CB_READONLY)
        self.encodingSizer.AddWindow(self.encodingSelect, 0, border=5,
            flag=wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.EXPAND)
        self.Layout()

    def __init__(self, parent):
        global main
        main = parent.GetGrandParent()
        self.__init_ctrls(parent)
        self.Fit()

    def init_enabled(self):
        self._set_encoding_options(1)
        self.dirTreeEnabled(1)

    def _set_encoding_options(self, event):
        Value = self.encodingGroup.GetStringSelection()
        enable = True
        if self.encodingSelect:
            self.encodingSelect.Destroy()
        if Value == _(u"Use System Default"):
            enable = False
        choicesList = utils.get_encoding_choices(Value)
        self.staticText2.Enable(True)
        self._make_encoding_select(choicesList)
        self.encodingSelect.SetSelection(0)
        if not enable:
            self.staticText2.Enable(False)
            self.encodingSelect.Enable(False)

    def dirTreeEnabled(self, event):
        if self.useDirTree.GetValue():
            allow = True
        else:
            allow = False
        self.showHiddenDirs.Enable(allow)
