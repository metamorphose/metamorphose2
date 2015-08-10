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

import insertTools
from notebook import Notebook
from operation import Operation
import utils
import wx


class OpPanel(Operation):
    """This panel controls inserts."""
    
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
        self.insertToolsPanel = insertTools.Panel(self.notebook, main)
        self.notebook.init_pages(self.insertToolsPanel,
                                 _(u"Insert settings"), u'insert.ico')
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
        self.insertToolsPanel.activate_options(False)
        self.numberingPanel.on_config_load()
        self.dateTimePanel.get_from_item_checkbox(False)

    def reset_counter(self, c):
        """Reset the numbering counter for the operation."""
        utils.reset_counter(self, self.insertToolsPanel, c)

    def rename_item(self, path, name, ext, original):
        """Insert into name."""
        newName = self.join_ext(name, ext)
        if not newName:
            return path, name, ext

        insert = self.insertToolsPanel
        operations = insert.opButtonsPanel
        parsedText = operations.parse_input(insert.Text.GetValue(), original, self)
        # prefix
        if insert.prefix.GetValue():
            newName = parsedText + name
        # suffix
        elif insert.suffix.GetValue():
            newName = name + parsedText
        # exact position
        elif insert.position.GetValue():
            pos = insert.positionPos.GetValue()
            if pos == -1:
                newName += parsedText
            elif pos < -1:
                newName = newName[:pos + 1] + parsedText + newName[pos + 1:]
            else:
                newName = newName[:pos] + parsedText + newName[pos:]

        # insert before/after a character:
        elif insert.after.GetValue() or insert.before.GetValue():
            good2go = False
            textMatch = insert.BAtextMatch.GetValue()
            # text search
            if not insert.regExpPanel.regExpr.GetValue():
                try:
                    insertAt = newName.index(textMatch)
                except ValueError:
                    pass
                else:
                    if insert.after.GetValue():
                        insertAt += len(textMatch)
                    good2go = True
            # regular expression search
            else:
                insertRE = insert.regExpPanel.create_regex(textMatch)
                try:
                    insertAt = insertRE.search(newName).end()
                except AttributeError:
                    pass
                else:
                    if insert.before.GetValue():
                        insertAt -= len(textMatch)
                    good2go = True

            if good2go:
                newName = newName[:insertAt] + parsedText + newName[insertAt:]

        # insert in between 2 characters:
        # (copy of search.py function)
        elif insert.between.GetValue():
            good2go = False
            if insert.regExpPanel.regExpr.GetValue():
                mod1 = insert.regExpPanel.create_regex(insert.BTWtextMatch1.GetValue())
                mod2 = insert.regExpPanel.create_regex(insert.BTWtextMatch2.GetValue())
                try:
                    frm = mod1.search(newName).end()
                    to = mod2.search(newName, frm).start()
                except AttributeError:
                    pass
                else:
                    good2go = True
            else:
                match1 = insert.BTWtextMatch1.GetValue()
                match2 = insert.BTWtextMatch2.GetValue()
                try:
                    frm = newName.index(match1) + len(match1)
                    to = newName.index(match2, frm)
                except ValueError:
                    pass
                else:
                    good2go = True
            if good2go:
                newName = newName[:frm] + parsedText + newName[to:]

        name, ext = self.split_ext(newName, name, ext)

        return path, name, ext
