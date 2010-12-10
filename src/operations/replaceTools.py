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
import opButtons
import search

[wxID_PANEL, wxID_PANELREPL_TXT, wxID_PANELSTATICTEXT1, wxID_PANELSTATICBOX1
] = [wx.NewId() for __init_ctrls in range(4)]

class Panel(wx.Panel):
    """This is the panel in charge of replacing matches with text or operations."""
    
    def __init_sizer(self):
        mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer.Add(self.staticText1,0,wx.ALIGN_CENTRE|wx.LEFT,5)
        bottomSizer.Add(self.repl_txt,1,wx.LEFT|wx.RIGHT,5)

        replaceWithSizer = wx.StaticBoxSizer(self.staticBox1, wx.VERTICAL)
        replaceWithSizer.AddSizer(bottomSizer,0,wx.EXPAND|wx.TOP,5)
        replaceWithSizer.Add(self.opButtonsPanel,0,wx.EXPAND|wx.TOP|wx.BOTTOM,2)

        mainSizer.Add(self.search,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
        mainSizer.AddSpacer((1,5))
        mainSizer.AddSizer(replaceWithSizer,0,wx.EXPAND|wx.ALL,5)
        self.SetSizerAndFit(mainSizer)

    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_PANEL, name=u'ReplaceToolsPanel', parent=prnt,
              style=wx.TAB_TRAVERSAL)
              
        self.search = search.Panel(self, main, _(u"Search for what to replace, by:"))

        self.staticBox1 = wx.StaticBox(id=wxID_PANELSTATICBOX1,
              label=_("Replace with:"), name='staticBox1', parent=self, style=0)

        # sub operation buttons ------------------------------------------- #
        self.opButtonsPanel = opButtons.Panel(self, main)

        txt = _(u"Text (blank to delete):")
        self.staticText1 = wx.StaticText(id=wxID_PANELSTATICTEXT1,
              label=txt, name='staticText1',
              parent=self, style=0)
        Size = wx.Size(self.staticText1.GetTextExtent(txt)[0] + 3,-1)
        self.staticText1.SetMinSize(Size)

        self.repl_txt = wx.TextCtrl(id=wxID_PANELREPL_TXT,
              name=u'repl_txt', parent=self,
              style=wx.TE_PROCESS_ENTER, value=u'')
        self.repl_txt.SetToolTipString(_(u"Keep blank to delete."))
        self.repl_txt.Bind(wx.EVT_TEXT, main.show_preview)
        self.repl_txt.Bind(wx.EVT_TEXT_ENTER, main.show_preview)

    def __init__(self, parent, main_window, params={}):
        global main
        main = main_window
        self.__init_ctrls(parent)
        self.__init_sizer()
        self.on_load()

    def on_load(self):
        self.activatedField = self.repl_txt
        self.search.on_load(0)
