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

import wx
from operation import Operation
import search
import utils

[wxID_PANEL, wxID_PANELREPL_MOVE_POS, wxID_PANELREPL_MOVE_POS_VALUE,
 wxID_PANELREPL_MOVE_TXT, wxID_PANELREPL_MOVE_TXT_MOD,
 wxID_PANELREPL_MOVE_TXT_RE, wxID_PANELREPL_MOVE_TXT_VALUE,
 wxID_PANELSTATICTEXT6, wxID_PANELSTATICBOX1, wxID_PANELREPL_MOVE_TXT_REU,
 wxID_PANELREPL_MOVE_TXT_REI, wxID_PANELSTATICTEXT5
] = [wx.NewId() for __init_ctrls in range(12)]

class OpPanel(Operation):
    """
    Panel to hold swap widgets and operations.
    Uses search panel.
    """
    def __init_sizer(self):
        mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.searchFrom,0,wx.EXPAND|wx.BOTTOM,3)
        mainSizer.Add(self.searchTo,0,wx.EXPAND)
        self.SetSizerAndFit(mainSizer)


    def __init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANEL, name=u'Panel', parent=prnt,
              style=wx.TAB_TRAVERSAL)

        self.searchFrom = search.Panel(self, main, _(u"Swap this:"), 'searchFrom')
        self.searchTo = search.Panel(self, main, _(u"With this:"), 'searchTo')

    def __init__(self, parent, main_window, params={}):
        Operation.__init__(self, params)
        global main
        main = main_window
        self.__init_ctrls(parent)
        self.__init_sizer()

    def on_config_load(self):
        self.searchTo.on_load(0)
        self.searchFrom.on_load(0)

    def find_in_name(self, newName, search, searchValues):
        # regular expression:
        frm = 0
        to = 0
        if searchValues[0] == u"reg-exp" and searchValues[1]:
            try:
                match = searchValues[2].findall(newName)[0]
                frm = newName.index(match)
                to = frm + len(match)
            except (AttributeError, IndexError):
                pass
            # show RE error message from search, if any
            if search.REmsg:
                main.set_status_msg(search.REmsg,u'warn')
                app.REmsg = True

        # text:
        elif searchValues[0] == u"text" and searchValues[2]:
            #case insensitive
            if not searchValues[1]:
                found = search.case_insensitive(newName)
                if len(found) > 0:
                    match = found[0]
                    frm = newName.index(match)
                    to = frm + len(match)
            # case sensitive
            elif searchValues[2] in newName:
                match = searchValues[2]
                frm = newName.index(match)
                to = frm + len(match)

        # position
        elif searchValues[0] == u"position":
            ss = search.repl_from.GetValue()
            sl = search.repl_len.GetValue()
            frm,to = utils.calc_slice_pos(ss,sl)

        # between
        elif searchValues[0] == u"between":
            positions = search.get_between_to_from(newName)
            if positions:
                frm = positions[0]
                to = positions[1]

        return (frm,to)

    def rename_item(self, path, name, ext, original):
        newName = self.join_ext(name,ext)
        if not newName:
            return path,name,ext

        # basic settings
        searchFrom = self.searchFrom
        searchFromValues = searchFrom.searchValues

        searchTo = self.searchTo
        searchToValues = searchTo.searchValues

        # now find what to swap
        swapMatchFrom = self.find_in_name(newName, searchFrom, searchFromValues)
        swapMatchTo = self.find_in_name(newName, searchTo, searchToValues)

        # only works for one character for now
        if swapMatchFrom != (0,0) and swapMatchTo != (0,0) and swapMatchTo != swapMatchFrom:
            swapMatchTo1 = newName[swapMatchTo[0]:swapMatchTo[1]]
            swapMatchFrom1 = newName[swapMatchFrom[0]:swapMatchFrom[1]]
            newNameList = []
            for c in newName:
                newNameList.append(c)
            # need to incorporate the length better
            newNameList[swapMatchFrom[0]:swapMatchFrom[1]] = swapMatchTo1
            newNameList[swapMatchTo[0]:swapMatchTo[1]] = swapMatchFrom1
            newName = ""
            for c in newNameList:
                newName += c

        #---- code goes here ----

        name,ext = self.split_ext(newName,name,ext)
        return path,name,ext


