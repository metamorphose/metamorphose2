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

import regExpr
import utils
import wx

[wxID_PANEL, wxID_PANELREPL_CASE, wxID_PANELREPL_FIND,
    wxID_PANELREPL_FROM, wxID_PANELREPL_POSBUTTON,
    wxID_PANELREPL_TEXTBUTTON, wxID_PANELREPL_LEN,
    wxID_PANELSTATICTEXT2, wxID_PANELSTATICBOX1,
    wxID_PANELBETWEEN, wxID_PANELBTWTEXTMATCH1,
    wxID_PANELBTWTEXTMATCH2, wxID_PANELSTATICTEXT6, wxID_PANELSTATICTEXT7,
    wxID_PANELSTATICTEXT1
] = [wx.NewId() for __init_ctrls in range(15)]

class Panel(wx.Panel):
    """
    Panel to hold searching widgets, and return search parameters
    to parent panel.
    """
    
    def __init_sizer(self):
        mainSizer = self.mainSizer = wx.StaticBoxSizer(self.staticBox1, wx.VERTICAL)
        #text
        mainSizer.Add(self.repl_textButton, 0, wx.EXPAND)
        textSizer = self.textSizer = wx.BoxSizer(wx.HORIZONTAL)
        textSizer.Add(self.repl_find, 75, wx.RIGHT, 10)
        textSizer.Add(self.repl_case, 0, wx.ALIGN_CENTER)
        textSizer.Add((-1, -1), 1)
        mainSizer.Add(textSizer, 0, wx.EXPAND)
        #in between
        btwSizer = wx.BoxSizer(wx.HORIZONTAL)
        btwSizer.Add(self.between, 0, wx.ALIGN_CENTRE | wx.RIGHT, 5)
        btwSizer.Add(self.staticText6, 0, wx.ALIGN_CENTRE)
        btwSizer.Add(self.BTWtextMatch1, 35, wx.LEFT, 2)
        btwSizer.Add((-1, -1), 1)
        btwSizer.Add(self.staticText7, 0, wx.ALIGN_CENTRE | wx.LEFT, 5)
        btwSizer.Add(self.BTWtextMatch2, 35, wx.LEFT, 2)
        btwSizer.Add((-1, -1), 1)
        mainSizer.Add(btwSizer, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 3)
        #regular expression
        mainSizer.Add(self.regExpPanel, 0, wx.EXPAND | wx.LEFT, 10)
        #position
        posSizer = self.posSizer = wx.BoxSizer(wx.HORIZONTAL)
        posSizer.Add(self.repl_posButton, 0, wx.ALIGN_CENTER | wx.RIGHT, 8)
        posSizer.Add(self.staticText1, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        posSizer.Add(self.repl_from, 0, wx.ALIGN_CENTER | wx.RIGHT, 8)
        posSizer.Add(self.staticText2, 0, wx.ALIGN_CENTER | wx.RIGHT, 4)
        posSizer.Add(self.repl_len, 0, wx.ALIGN_CENTER | wx.RIGHT, 20)
        mainSizer.Add(posSizer, 0, wx.EXPAND | wx.TOP, 10)

        self.SetSizerAndFit(mainSizer)


    def __init_ctrls(self, prnt, title, Name):
        wx.Panel.__init__(self, id=wxID_PANEL, name=Name, parent=prnt, style=0)

        self.staticBox1 = wx.StaticBox(id=wxID_PANELSTATICBOX1,
                                       label=title, name='staticBox1', parent=self, style=0)

        # regular expressions
        self.regExpPanel = regExpr.Panel(self, main)

        # text
        self.repl_textButton = wx.RadioButton(id=wxID_PANELREPL_TEXTBUTTON,
                                              label=_(u"Text (Keep blank to match entire name):"), name=u'repl_textButton',
                                              parent=self, style=wx.RB_GROUP)
        self.repl_textButton.SetValue(True)
        self.repl_textButton.Bind(wx.EVT_RADIOBUTTON,
                                  self.activate_options, id=wxID_PANELREPL_TEXTBUTTON)

        self.repl_find = wx.TextCtrl(id=wxID_PANELREPL_FIND, name=u'repl_find',
                                     parent=self, style=wx.TE_PROCESS_ENTER, value='')
        self.repl_find.Bind(wx.EVT_SET_FOCUS, self.regExpPanel.set_activated_field,
                            id=wxID_PANELREPL_FIND)
        self.repl_find.Bind(wx.EVT_TEXT, self.define_text)
        self.repl_find.Bind(wx.EVT_TEXT_ENTER, self.define_text)

        self.repl_case = wx.CheckBox(id=wxID_PANELREPL_CASE,
                                     label=_(u"case sensitive"), name=u'repl_case', parent=self,
                                     style=0)
        self.repl_case.SetValue(False)
        self.repl_case.SetToolTipString(_(u"Differentiate between upper and lower case"))
        self.repl_case.Bind(wx.EVT_CHECKBOX, self.define_text)

        # in between
        self.between = wx.RadioButton(id=wxID_PANELBETWEEN, label=_(u"In between"),
                                      name=u'between', parent=self, style=0)
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
        self.BTWtextMatch1.Bind(wx.EVT_TEXT, self.define_between,
                                id=wxID_PANELBTWTEXTMATCH1)
        self.BTWtextMatch1.Bind(wx.EVT_TEXT_ENTER, self.define_between,
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
        self.BTWtextMatch2.Bind(wx.EVT_TEXT, self.define_between,
                                id=wxID_PANELBTWTEXTMATCH2)
        self.BTWtextMatch2.Bind(wx.EVT_TEXT_ENTER, self.define_between,
                                id=wxID_PANELBTWTEXTMATCH2)

        # position
        self.repl_posButton = wx.RadioButton(id=wxID_PANELREPL_POSBUTTON,
                                             label=_(u"Fixed position"), name=u'repl_posButton', parent=self,
                                             style=0)
        self.repl_posButton.SetValue(False)
        self.repl_posButton.Bind(wx.EVT_RADIOBUTTON,
                                 self.activate_options, id=wxID_PANELREPL_POSBUTTON)

        self.staticText1 = wx.StaticText(id=wxID_PANELSTATICTEXT6,
                                         label=_(u"Starting at:"), name='staticText6', parent=self,
                                         style=0)
        self.staticText1.Enable(False)

        self.repl_from = wx.SpinCtrl(id=wxID_PANELREPL_FROM, initial=0, max=255,
                                     min=-255, name=u'repl_from', parent=self, size=wx.Size(65, -1),
                                     style=wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER, value='0')
        self.repl_from.SetValue(0)
        self.repl_from.Enable(False)
        self.repl_from.Bind(wx.EVT_TEXT_ENTER, main.show_preview)
        self.repl_from.Bind(wx.EVT_SPINCTRL, main.show_preview)

        self.staticText2 = wx.StaticText(id=wxID_PANELSTATICTEXT2,
                                         label=_(u"Selection length:"), name=u'repl_txt_to', parent=self,
                                         style=0)
        self.staticText2.Enable(False)

        self.repl_len = wx.SpinCtrl(id=wxID_PANELREPL_LEN, initial=1, max=255,
                                    min=1, name=u'repl_len', parent=self, size=wx.Size(65, -1),
                                    style=wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER, value='1')
        self.repl_len.Enable(False)
        self.repl_len.Bind(wx.EVT_TEXT_ENTER, main.show_preview,
                           id=wxID_PANELREPL_LEN)
        self.repl_len.Bind(wx.EVT_SPINCTRL, main.show_preview,
                           id=wxID_PANELREPL_LEN)

        # fix win2000 bug
        self.filler = wx.RadioButton(id=-1, label='', name=u'filler', parent=self, style=wx.RB_GROUP)
        self.filler.Show(False)

    def __init__(self, parent, main_window, title, name=u'search'):
        global main
        main = main_window
        self.__init_ctrls(parent, title, name)
        self.__init_sizer()
        self.on_load(0)

    def on_load(self, event):
        """Initial search definition."""
        self.define_text(0)
        self.regExpPanel.activatedField = self.repl_find
        self.activate_options(0)

    def define_regex(self, event):
        """Create and compile regular expressions, set required variables"""
        if self.repl_textButton.GetValue():
            self.define_text(event)
        elif self.between.GetValue():
            self.define_between(event)

    def define_between(self, event):
        """Set variables for between search."""
        self.searchValues = (u"between", )
        if self.regExpPanel.regExpr.GetValue():
            self.mod1 = self.regExpPanel.create_regex(self.BTWtextMatch1.GetValue())
            self.mod2 = self.regExpPanel.create_regex(self.BTWtextMatch2.GetValue())
        main.show_preview(event)

    def get_between_to_from(self, newName):
        """Calculate between positions."""
        if self.regExpPanel.regExpr.GetValue():
            try:
                frm = self.mod1.search(newName).end()
                to = self.mod2.search(newName, frm).start()
            except AttributeError:
                return False
            else:
                return (frm, to)
        else:
            match1 = self.BTWtextMatch1.GetValue()
            match2 = self.BTWtextMatch2.GetValue()
            try:
                frm = newName.index(match1) + len(match1)
                to = newName.index(match2, frm)
            except ValueError:
                return False
            else:
                return (frm, to)

    def define_text(self, event):
        """Set necessary variables for text search."""
        if self.regExpPanel.regExpr.GetValue():
            REfind = self.repl_find.GetValue()
            # need a value
            if REfind == '':
                REfind = u'.*'
            mod = self.regExpPanel.create_regex(REfind)
            self.searchValues = (u"reg-exp", REfind, mod)
        else:
            find = self.repl_find.GetValue()
            # - case sensitive
            if self.repl_case.GetValue():
                self.searchValues = (u"text", True, find)
            #- case insensitive
            else:
                self.searchValues = (u"text", False, find)
        main.show_preview(event)

    def case_insensitive(self, newName):
        """Case insensitive search."""
        CIfind = self.repl_find.GetValue().lower()
        CIrenamed = newName.lower()
        found = []
        # no need to run whole operation if not found at all:
        if CIfind in CIrenamed:
            find_len = len(CIfind)
            if find_len == 0:
                find_len = 1
            renamed_len = len(CIrenamed)
            #get matching sections:
            index = 0
            x = 0
            while x < renamed_len:
                try:
                    x = CIrenamed.index(CIfind, index, renamed_len)
                except ValueError:
                    break
                else:
                    index = x + find_len
                    found.append(newName[x:index])
        return found

    def __define_position(self, event):
        """Create the positions and define variables."""
        self.searchValues = (u"position", 0, 0)
        main.show_preview(event)

    def get_start_end_pos(self, ss, sl, newName):
        """Get the start and end positions of the given name."""
        frm, to = utils.calc_slice_pos(ss, sl)
        if to == None:
            tail = ''
        else:
            tail = newName[to:]
        return frm, to, tail

    def activate_options(self, event):
        """Activate widgets based on user input."""
        # find text field and case insensitive chekbox:
        repl_text_tup = (self.repl_find, self.repl_case)
        if self.repl_textButton.GetValue():
            for option in repl_text_tup:
                option.Enable(True)
            # define the text
            self.repl_find.SetFocus()
            self.regExpPanel.regExpr.Enable(True)
            self.define_text(0)
        else:
            for option in repl_text_tup:
                option.Enable(False)

        # in between widgets
        between_tup = (self.staticText6, self.staticText7,
                       self.BTWtextMatch1, self.BTWtextMatch2)
        if self.between.GetValue():
            for option in between_tup:
                option.Enable(True)
            # define the between position
            self.BTWtextMatch1.SetFocus()
            self.define_between(0)
            self.regExpPanel.regExpr.Enable(True)
        else:
            for option in between_tup:
                option.Enable(False)

        # positioning widgets
        repl_pos_tup = (self.repl_from, self.staticText1, self.staticText2,
                        self.repl_len)
        if self.repl_posButton.GetValue():
            for option in repl_pos_tup:
                option.Enable(True)
            # define the position
            self.__define_position(0)
            self.regExpPanel.regExpr.Enable(False)
        else:
            for option in repl_pos_tup:
                option.Enable(False)

        # regular expression widgets:
        if self.regExpPanel.regExpr.GetValue() and self.regExpPanel.regExpr.IsEnabled():
            self.regExpPanel.set_active(True)
            self.repl_case.Enable(False)
        else:
            self.regExpPanel.set_active(False)

        if hasattr(self.GetParent(), 'CreateOperation') and event:
            self.GetParent().CreateOperation(event)
        else:
            main.show_preview(event)
