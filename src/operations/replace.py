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

import sre_constants

from notebook import Notebook
from operation import Operation
import replaceTools
import utils
import wx

class OpPanel(Operation):
    """Panel in charge of replacing matches with text or operations."""

    def __init_sizer(self, parent):
        #smallestSize = parent.rightSizer.GetSize() - parent.rightTopSizer.GetSize() - (10,10)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        #mainSizer.SetMinSize(smallestSize)
        mainSizer.Add(self.notebook, 0, wx.EXPAND)
        self.SetSizerAndFit(mainSizer)

    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=-1, name=u'Panel', parent=prnt,
                          style=wx.TAB_TRAVERSAL)
        self.notebook = Notebook(self, main)
        self.replaceToolsPanel = replaceTools.Panel(self.notebook, main)
        self.notebook.init_pages(self.replaceToolsPanel,
                                 _(u"Replace settings"), u'replace.ico')
        self.numberingPanel = self.notebook.numbering
        self.dateTimePanel = self.notebook.dateTime


    def __init__(self, parent, main_window, params={}):
        Operation.__init__(self, params)
        global main
        main = main_window
        self.__init_ctrls(parent)
        self.__init_sizer(parent)

    def on_config_load(self):
        """Update GUI elements, settings after config load."""
        self.replaceToolsPanel.on_load()
        self.numberingPanel.on_config_load()
        self.dateTimePanel.get_from_item_checkbox(False)

    def reset_counter(self, c):
        """Reset the numbering counter for the operation."""
        utils.reset_counter(self, self.replaceToolsPanel, c)

    def rename_item(self, path, name, ext, original):
        operations = self.replaceToolsPanel.opButtonsPanel
        newName = self.join_ext(name, ext)
        if not newName:
            return path, name, ext

        # basic settings
        search = self.replaceToolsPanel.search
        searchValues = search.searchValues
        text = self.replaceToolsPanel.repl_txt.GetValue()

        #- do nothing
        if searchValues[0] == u"text" and not searchValues[2] and not text:
            return path, name, ext

        #- search and replace when field not blank:
        elif searchValues[0] == u"text" and searchValues[2]:
            find = searchValues[2]
            parsedText = operations.parse_input(text, original, self)
            #case insensitive
            if not searchValues[1]:
                found = search.case_insensitive(newName)
                for match in found:
                    newName = newName.replace(match, parsedText)
            #case sensitive:
            else:
                newName = newName.replace(find, parsedText)
        
        #- replace everything if text field is blank:
        elif searchValues[0] == u"text":
            newName = operations.parse_input(text, original, self)

        #- replace using regular expression:
        elif searchValues[0] == u"reg-exp" and searchValues[1]:
            # need to first substiute, then parse for backreference support
            try:
                replaced = searchValues[2].sub(text, newName)
            except (sre_constants.error, AttributeError) as err:
                main.set_status_msg(_(u"Regular-Expression: %s") % err, u'warn')
                # so we know not to change status text after RE error msg:
                app.REmsg = True
                pass
            else:
                newName = operations.parse_input(replaced, original, self)

            # show RE error message from search, if any
            if search.REmsg:
                main.set_status_msg(search.REmsg, u'warn')
                app.REmsg = True

        #- replace in between
        elif searchValues[0] == u"between":
            positions = search.get_between_to_from(newName)
            if positions:
                frm = positions[0]
                to = positions[1]
                parsedText = operations.parse_input(text, original, self)
                newName = newName[:frm] + parsedText + newName[to:]

        #- replace by position:
        elif searchValues[0] == u"position":
            ss = search.repl_from.GetValue()
            sl = search.repl_len.GetValue()
            frm, to, tail = search.get_start_end_pos(ss, sl, newName)
            parsedText = operations.parse_input(text, original, self)
            newName = newName[:frm] + parsedText + tail

        name, ext = self.split_ext(newName, name, ext)
        return path, name, ext