# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2011 ianaré sévi <ianare@gmail.com>
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

import platform
import sys

import opButtons
import regExpr
import wx

[wxID_PANEL, wxID_PANELAFTER, wxID_PANELBARE, wxID_PANELBAREI,
	wxID_PANELBAREU, wxID_PANELBATEXTMATCH, wxID_PANELBEFORE,
	wxID_PANELPOSITION, wxID_PANELPOSITIONPOS, wxID_PANELPOSITIONTEXT,
	wxID_PANELPREFIX, wxID_PANELTEXT, wxID_PANELSTATICBOX1,
	wxID_PANELSTATICTEXT4, wxID_PANELSTATICTEXT5,
	wxID_PANELSUFFIX, wxID_PANELBETWEEN, wxID_PANELBTWTEXTMATCH1,
	wxID_PANELBTWTEXTMATCH2, wxID_PANELBTWRE, wxID_PANELBTWREI,
	wxID_PANELBTWREU, wxID_PANELSTATICTEXT6, wxID_PANELSTATICTEXT7
] = [wx.NewId() for __init_ctrls in range(24)]

class Panel(wx.Panel):
    """This panel allows inserting text or operations."""
    
    def __init_sizer(self):
        rowB = wx.BoxSizer(wx.HORIZONTAL)
        rowB.Add(self.prefix, 0, wx.ALIGN_CENTRE | wx.LEFT, 5)
        rowB.Add(self.suffix, 0, wx.ALIGN_CENTRE | wx.LEFT, 15)
        rowB.Add(self.position, 0, wx.ALIGN_CENTRE | wx.LEFT, 15)
        rowB.Add(self.positionPos, 0, wx.LEFT, 2)

        rowC = wx.BoxSizer(wx.HORIZONTAL)
        rowC.Add(self.before, 0, wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT, 5)
        rowC.Add(self.after, 0, wx.ALIGN_CENTRE | wx.RIGHT, 10)
        rowC.Add(self.staticText5, 0, wx.ALIGN_CENTRE | wx.RIGHT, 3)
        rowC.Add(self.BAtextMatch, 1, wx.RIGHT, 8)

        rowD = wx.BoxSizer(wx.HORIZONTAL)
        rowD.Add(self.between, 0, wx.ALIGN_CENTRE | wx.LEFT, 5)
        rowD.Add(self.staticText6, 0, wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT, 5)
        rowD.Add(self.BTWtextMatch1, 1, wx.LEFT, 2)
        rowD.Add(self.staticText7, 0, wx.ALIGN_CENTRE | wx.LEFT, 5)
        rowD.Add(self.BTWtextMatch2, 1, wx.LEFT | wx.RIGHT, 2)

        superSizer = wx.BoxSizer(wx.VERTICAL)
        superSizer.Add(self.opButtonsPanel, 0, wx.EXPAND)
        superSizer.Add((-1, 20), 0)
        superSizer.Add(self.staticText4, 0, wx.LEFT, 5)
        superSizer.Add(self.Text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 3)
        superSizer.Add(rowB, 0, wx.EXPAND | wx.TOP, 20)
        superSizer.Add(rowC, 0, wx.EXPAND | wx.TOP, 20)
        superSizer.Add(rowD, 0, wx.EXPAND | wx.TOP, 10)
        superSizer.Add(self.regExpPanel, 0, wx.EXPAND | wx.TOP | wx.LEFT, 10)
        superSizer.Add((-1, 5), 0)

        self.SetSizerAndFit(superSizer)

    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_PANEL, name=u'insertToolsPanel',
						  parent=prnt, style=wx.TAB_TRAVERSAL)

        # regular expressions --------------------------------------------- #
        self.regExpPanel = regExpr.Panel(self, main)

        # sub operation buttons ------------------------------------------- #
        self.opButtonsPanel = opButtons.Panel(self, main)

        self.Text = wx.TextCtrl(id=wxID_PANELTEXT,
								name=u'Text', parent=self, style=wx.TE_PROCESS_ENTER, value=u'')
        self.Text.Bind(wx.EVT_TEXT, main.show_preview,
					   id=wxID_PANELTEXT)

        self.staticText4 = wx.StaticText(id=wxID_PANELSTATICTEXT4,
										 label=_(u"Add this:"), name='staticText4', parent=self,
										 style=0)
        self.staticText4.Enable(True)

        self.prefix = wx.RadioButton(id=wxID_PANELPREFIX,
									 label=_(u"As a prefix"), name=u'prefix', parent=self,
									 style=wx.RB_GROUP)
        self.prefix.SetValue(True)
        self.prefix.Bind(wx.EVT_RADIOBUTTON, self.activate_options,
						 id=wxID_PANELPREFIX)

        self.suffix = wx.RadioButton(id=wxID_PANELSUFFIX,
									 label=_(u"As a suffix"), name=u'suffix', parent=self,
									 style=0)
        self.suffix.SetValue(False)
        self.suffix.Bind(wx.EVT_RADIOBUTTON, self.activate_options,
						 id=wxID_PANELSUFFIX)

        self.position = wx.RadioButton(id=wxID_PANELPOSITION,
									   label=_(u"At this position:"), name=u'position', parent=self,
									   style=0)
        self.position.SetValue(False)
        self.position.Bind(wx.EVT_RADIOBUTTON, self.activate_options,
						   id=wxID_PANELPOSITION)

        self.positionPos = wx.SpinCtrl(id=wxID_PANELPOSITIONPOS, initial=0,
									   max=255, min=-255, name=u'positionPos', parent=self,
									   size=wx.Size(56, -1), style=wx.SP_ARROW_KEYS, value='0')
        self.positionPos.SetToolTipString(_(u"Use negative values to start from the end of the name."))
        self.positionPos.Enable(False)
        self.positionPos.Bind(wx.EVT_SPINCTRL, main.show_preview,
							  id=wxID_PANELPOSITIONPOS)

        self.before = wx.RadioButton(id=wxID_PANELBEFORE, label=_(u"Before"),
									 name=u'before', parent=self, style=0)
        self.before.SetValue(False)
        self.before.Bind(wx.EVT_RADIOBUTTON, self.activate_options,
						 id=wxID_PANELBEFORE)

        self.after = wx.RadioButton(id=wxID_PANELAFTER, label=_(u"After"),
									name=u'after', parent=self, style=0)
        self.after.SetValue(False)
        self.after.Bind(wx.EVT_RADIOBUTTON, self.activate_options,
						id=wxID_PANELAFTER)

        self.staticText5 = wx.StaticText(id=wxID_PANELSTATICTEXT5,
										 label=_(u"this text:"), name='staticText5', parent=self,
										 style=0)
        self.staticText5.Enable(False)

        self.BAtextMatch = wx.TextCtrl(id=wxID_PANELBATEXTMATCH,
									   name=u'BAtextMatch', parent=self, style=wx.TE_PROCESS_ENTER,
									   value=u'')
        self.BAtextMatch.Enable(False)
        self.BAtextMatch.Bind(wx.EVT_SET_FOCUS, self.regExpPanel.set_activated_field,
							  id=wxID_PANELBATEXTMATCH)
        self.BAtextMatch.Bind(wx.EVT_TEXT, main.show_preview,
							  id=wxID_PANELBATEXTMATCH)
        self.BAtextMatch.Bind(wx.EVT_TEXT_ENTER, main.show_preview,
							  id=wxID_PANELBATEXTMATCH)

        self.between = wx.RadioButton(id=wxID_PANELBETWEEN, label=_(u"In between"),
									  name=u'between', parent=self, style=0)
        self.between.Enable(True)
        self.between.SetValue(False)
        self.between.Bind(wx.EVT_RADIOBUTTON, self.activate_options,
						  id=wxID_PANELBETWEEN)

        self.staticText6 = wx.StaticText(id=wxID_PANELSTATICTEXT6,
										 label=_(u"this text:"), name='staticText6', parent=self,
										 style=0)
        self.staticText6.Enable(False)

        self.BTWtextMatch1 = wx.TextCtrl(id=wxID_PANELBTWTEXTMATCH1,
										 name=u'BTWtextMatch1', parent=self,
										 style=wx.TE_PROCESS_ENTER, value=u'')
        self.BTWtextMatch1.Enable(False)
        self.BTWtextMatch1.Bind(wx.EVT_SET_FOCUS, self.regExpPanel.set_activated_field,
								id=wxID_PANELBTWTEXTMATCH1)
        self.BTWtextMatch1.Bind(wx.EVT_TEXT, main.show_preview,
								id=wxID_PANELBTWTEXTMATCH1)
        self.BTWtextMatch1.Bind(wx.EVT_TEXT_ENTER, main.show_preview,
								id=wxID_PANELBTWTEXTMATCH1)

        self.staticText7 = wx.StaticText(id=wxID_PANELSTATICTEXT7,
										 label=_(u"and this text:"), name='staticText7', parent=self,
										 style=0)
        self.staticText7.Enable(False)

        self.BTWtextMatch2 = wx.TextCtrl(id=wxID_PANELBTWTEXTMATCH2,
										 name=u'BTWtextMatch2', parent=self,
										 style=wx.TE_PROCESS_ENTER, value=u'')
        self.BTWtextMatch2.Enable(False)
        self.BTWtextMatch2.Bind(wx.EVT_SET_FOCUS, self.regExpPanel.set_activated_field,
								id=wxID_PANELBTWTEXTMATCH2)
        self.BTWtextMatch2.Bind(wx.EVT_TEXT, main.show_preview,
								id=wxID_PANELBTWTEXTMATCH2)
        self.BTWtextMatch2.Bind(wx.EVT_TEXT_ENTER, main.show_preview,
								id=wxID_PANELBTWTEXTMATCH2)

        # grotesque hack for win2000
        if platform.system() == 'Windows':
            winver = sys.getwindowsversion()
            if winver[0] <= 5 and winver[1] < 1:
                self.hack = wx.RadioButton(id=-1, label='',
										   name=u'hack', parent=self, style=wx.RB_GROUP)
                self.hack.Show(False)

    def __init__(self, parent, main_window):
        global main
        main = main_window
        self.__init_ctrls(parent)
        self.__init_sizer()
        self.activatedField = self.Text
        self.regExpPanel.activatedField = self.BAtextMatch
        self.activate_options(False)

    def define_regex(self, event):
        """
        Compile regexp and create required values.
        """
        if self.before.GetValue() or self.after.GetValue():
            self.define_text(event)
        elif self.between.GetValue():
            self.define_between(event)

    def activate_options(self, event):
        """Activate or disactivate fields based on user selection."""
        useRE = False
        if self.position.GetValue():
            self.positionPos.Enable(True)
        else:
            self.positionPos.Enable(False)

        find = (self.staticText5, self.BAtextMatch)
        if self.before.GetValue() or self.after.GetValue():
            for i in find: i.Enable(True)
            useRE = True
            self.regExpPanel.activatedField = self.BAtextMatch
        else:
            for i in find: i.Enable(False)

        find = (self.staticText6, self.BTWtextMatch1, self.staticText7,
				self.BTWtextMatch2)
        if self.between.GetValue():
            for i in find: i.Enable(True)
            useRE = True
            self.regExpPanel.activatedField = self.BTWtextMatch1
        else:
            for i in find: i.Enable(False)

        if useRE:
            self.regExpPanel.regExpr.Enable(True)
            self.regExpPanel.set_active(True)
        else:
            self.regExpPanel.regExpr.Enable(False)
            self.regExpPanel.set_active(False)
        main.show_preview(event)
