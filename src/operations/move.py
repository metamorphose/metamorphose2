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

import platform
import sys

from operation import Operation
import regExpr
import search
import utils
import wx

[wxID_PANEL, wxID_PANELREPL_MOVE_POS, wxID_PANELREPL_MOVE_POS_VALUE,
    wxID_PANELREPL_MOVE_TXT, wxID_PANELREPL_MOVE_TXT_MOD,
    wxID_PANELREPL_MOVE_TXT_VALUE, wxID_PANELSTATICTEXT6, wxID_PANELSTATICBOX1,
    wxID_PANELSTATICTEXT5
 ] = [wx.NewId() for __init_ctrls in range(9)]


class OpPanel(Operation):
    """
    Panel to hold move widgets and operations.

    Uses search panel.
    """
    def __init_sizer(self):
        mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.search, 0, wx.EXPAND | wx.BOTTOM | wx.TOP, 10)

        moveSizer1 = self.moveSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        moveSizer1.Add(self.replMovePos, 0, wx.ALIGN_CENTER | wx.LEFT, 5)
        moveSizer1.Add(self.replMovePosValue, 0, wx.ALIGN_CENTER | wx.LEFT, 5)
        moveSizer1.Add(self.staticText5, 0, wx.ALIGN_CENTER | wx.LEFT, 10)

        moveSizer2 = self.moveSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        moveSizer2.Add(self.replMoveText, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5)
        moveSizer2.Add(self.replMoveTextMod, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        moveSizer2.Add(self.staticText6, 0, wx.ALIGN_CENTER | wx.RIGHT, 3)
        moveSizer2.Add(self.replMoveTextValue, 1, wx.ALIGN_CENTER | wx.RIGHT, 5)

        moveSizer = self.moveSizer = wx.StaticBoxSizer(self.staticBox1, wx.VERTICAL)
        moveSizer.Add(moveSizer1, 0, wx.EXPAND | wx.TOP, 5)
        moveSizer.Add(moveSizer2, 0, wx.EXPAND | wx.TOP, 15)
        moveSizer.Add((-1, 5), 0)
        moveSizer.Add(self.regExpPanel, 0, wx.LEFT | wx.EXPAND, 15)
        moveSizer.Add((-1, 5), 0)

        mainSizer.Add(self.moveSizer, 0, wx.EXPAND)
        self.SetSizerAndFit(mainSizer)

    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_PANEL, name=u'Panel', parent=prnt,
                          style=0)

        # regular expressions --------------------------------------------- #
        self.regExpPanel = regExpr.Panel(self, main)

        self.search = search.Panel(self, main, _(u"Search for what to move, by:"))

        self.staticBox1 = wx.StaticBox(id=wxID_PANELSTATICBOX1,
                                       label=_(u"Move the match:"), name='staticBox1', parent=self,
                                       style=0)

        self.replMovePos = wx.RadioButton(id=wxID_PANELREPL_MOVE_POS,
                                          label=_(u"to position:"), name=u'replMovePos', parent=self,
                                          style=wx.RB_GROUP)
        self.replMovePos.SetValue(True)
        self.replMovePos.Bind(wx.EVT_RADIOBUTTON, self.activate_options,
                              id=wxID_PANELREPL_MOVE_POS)

        self.replMovePosValue = wx.SpinCtrl(id=wxID_PANELREPL_MOVE_POS_VALUE,
                                            initial=0, max=255, min=-255, name=u'replMovePosValue',
                                            parent=self, size=wx.Size(60, -1), value='0',
                                            style=wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER)
        self.replMovePosValue.SetValue(0)
        self.replMovePosValue.Bind(wx.EVT_TEXT_ENTER, main.show_preview,
                                   id=wxID_PANELREPL_MOVE_POS_VALUE)
        self.replMovePosValue.Bind(wx.EVT_SPINCTRL, main.show_preview,
                                   id=wxID_PANELREPL_MOVE_POS_VALUE)

        self.staticText5 = wx.StaticText(id=wxID_PANELSTATICTEXT6,
                                         label=_(u"Use negative values to start from end of name."),
                                         name=u'staticText5', parent=self, style=0)
        self.staticText5.Enable(True)

        self.replMoveText = wx.RadioButton(id=wxID_PANELREPL_MOVE_TXT,
                                           label=_(u"to"), name=u'replMoveText', parent=self, style=0)
        self.replMoveText.SetValue(False)
        self.replMoveText.Bind(wx.EVT_RADIOBUTTON, self.activate_options,
                               id=wxID_PANELREPL_MOVE_TXT)

        self.replMoveTextValue = wx.TextCtrl(id=wxID_PANELREPL_MOVE_TXT_VALUE,
                                             name=u'replMoveTextValue', parent=self, style=0, value='')
        self.replMoveTextValue.Enable(False)
        self.replMoveTextValue.Bind(wx.EVT_TEXT, main.show_preview,
                                    id=wxID_PANELREPL_MOVE_TXT_VALUE)

        self.replMoveTextMod = wx.Choice(choices=[_(u"before"), _(u"after"),
                                         _(u"replace")], id=wxID_PANELREPL_MOVE_TXT_MOD,
                                         name=u'replMoveTextMod', parent=self)
        self.replMoveTextMod.SetSelection(0)
        self.replMoveTextMod.Enable(False)
        self.replMoveTextMod.Bind(wx.EVT_CHOICE, main.show_preview,
                                  id=wxID_PANELREPL_MOVE_TXT_MOD)

        self.staticText6 = wx.StaticText(id=wxID_PANELSTATICTEXT6,
                                         label=_(u"text:"), name=u'staticText6', parent=self,
                                         style=0)
        self.staticText6.Enable(False)

        # grotesque hack for win2000
        if platform.system() == 'Windows':
            winver = sys.getwindowsversion()
            if winver[0] <= 5 and winver[1] < 1:
                self.hack = wx.RadioButton(id=-1, label='',
                                           name=u'hack', parent=self, style=wx.RB_GROUP)
                self.hack.Show(False)

    def __init__(self, parent, main_window, params={}):
        Operation.__init__(self, params)
        global main
        main = main_window
        self.__init_ctrls(parent)
        self.__init_sizer()
        self.activate_options(0)
        self.moveRE = False
        self.regExpPanel.activatedField = self.replMoveTextValue

    def activate_options(self, event):
        movetxt = (self.replMoveTextValue, self.replMoveTextMod, self.staticText6,
                   self.regExpPanel.regExpr)
        # by position
        if self.replMovePos.GetValue():
            self.replMovePosValue.Enable(True)
            for i in movetxt: i.Enable(False)
            self.staticText5.Enable(True)
            self.regExpPanel.set_active(False)
            self.moveRE = False
        # by text
        else:
            self.replMovePosValue.Enable(False)
            for i in movetxt: i.Enable(True)
            if self.regExpPanel.regExpr.GetValue():
                self.regExpPanel.set_active(True)
                #self.define_regex(event)
            self.staticText5.Enable(False)
        main.show_preview(event)

    def define_regex(self, event):
        moveTxt = self.replMoveTextValue.GetValue()
        self.moveRE = self.regExpPanel.create_regex(moveTxt)
        main.show_preview(event)

    def rename_item(self, path, name, ext, original):
        newName = self.join_ext(name, ext)
        if not newName:
            return path, name, ext

        # basic settings
        search = self.search
        searchValues = search.searchValues

        # calculate initial values
        moveTo = u':Do_Not_Move:'
        moveMod = self.replMoveTextMod.GetStringSelection()
        # by position:
        if self.replMovePos.GetValue():
            moveByPosition = True
            moveTo = self.replMovePosValue.GetValue()
        # by searching for text:
        else:
            moveByPosition = False
            moveTxt = self.replMoveTextValue.GetValue()
            # regular expression:
            if self.regExpPanel.regExpr.GetValue():
                self.moveRE = self.regExpPanel.create_regex(moveTxt)

        # default to not finding anything:
        moveMatch = ""

        # FIRST FIND THE ORIGINAL
        # regular expression:
        if searchValues[0] == u"reg-exp" and searchValues[1]:
            try:
                moveMatch = searchValues[2].findall(newName)[0]
            except (AttributeError, IndexError):
                pass
            # show RE error message from search, if any
            if search.REmsg:
                main.set_status_msg(search.REmsg, u'warn')
                app.REmsg = True
        # text:
        elif searchValues[0] == u"text" and searchValues[2]:
            find = searchValues[2]
            #case insensitive
            if not searchValues[1]:
                found = search.case_insensitive(newName)
                if len(found) > 0:
                    moveMatch = found[0]
            # case sensitive:
            elif find in newName:
                moveMatch = find
        # position
        elif searchValues[0] == u"position":
            ss = search.repl_from.GetValue()
            sl = search.repl_len.GetValue()
            frm, to = utils.calc_slice_pos(ss, sl)
            moveMatch = newName[frm:to]
        # between
        elif searchValues[0] == u"between":
            positions = search.get_between_to_from(newName)
            if positions:
                frm = positions[0]
                to = positions[1]
                moveMatch = newName[frm:to]

        # remove the original, saving a backup in case no match found:
        oldName = newName
        newName = newName.replace(moveMatch, "", 1)

        # now find where to move to if not by position:
        if not moveByPosition:
            if moveTxt: # text has to contain something
                # regular expression:
                if self.moveRE:
                    moveTxt = self.moveRE.findall(newName)
                    # if match is found, get first item in list:
                    if len(moveTxt) > 0:
                        moveTxt = moveTxt[0]
                    else:
                        moveTxt = ''
                # get the index of match:
                try:
                    moveTo = newName.index(moveTxt)
                except (ValueError):
                    moveTo = u':Do_Not_Move:'
                    pass
                else:
                    if moveMod == _(u"after"):
                        moveTo = moveTo + len(moveTxt)
                    elif moveMod != _(u"before"):
                        moveTo = moveMod
            else:
                moveTo = u':Do_Not_Move:'

        # finally recreate string:
        if moveTo != u':Do_Not_Move:':
            # position specified:
            if moveTo != moveMod and moveByPosition:
                if moveTo == -1:
                    newName = newName + moveMatch
                elif moveTo < -1:
                    newName = newName[:moveTo + 1] + moveMatch + newName[moveTo + 1:]
                else:
                    newName = newName[:moveTo] + moveMatch + newName[moveTo:]
            # text specified
            else:
                if moveTo == _(u"replace") and moveMatch:
                    newName = newName.replace(moveTxt, moveMatch, 1)
                elif moveMatch:
                    newName = newName[:moveTo] + moveMatch + newName[moveTo:]
            del oldName
        # no match found
        else:
            newName = oldName

        name, ext = self.split_ext(newName, name, ext)
        return path, name, ext
