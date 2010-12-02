# -*- coding: utf-8 -*-

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


[wxID_EDITDIALOG, wxID_EDITDIALOGBUTTON1, wxID_EDITDIALOGBUTTON2,
 wxID_EDITDIALOGSTATICTEXT1, wxID_EDITDIALOGSTATICTEXT2, wxID_EDITDIALOGVALUE,
 wxID_EDITDIALOGSTATICTEXT3
] = [wx.NewId() for __init_ctrls in range(7)]

class Dialog(wx.Dialog):
    def initCollBoxSizer1Items(self, parent):
        parent.AddSpacer(5)
        parent.AddWindow(self.staticText1, 0, border=4, flag=wx.ALL)
        parent.AddWindow(self.staticText2, 0, border=4, flag=wx.ALL)
        parent.AddWindow(self.staticText3, 0, border=4, flag=wx.ALL)
        parent.AddWindow(self.value, 0, border=5, flag=wx.ALL | wx.EXPAND)
        parent.AddSizer(self.boxSizer2, 0, border=10,
              flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM | wx.TOP | wx.EXPAND)

    def initCollBoxSizer2Items(self, parent):
        parent.AddWindow(self.backward, 0, border=5, flag=wx.LEFT)
        parent.AddStretchSpacer(1)
        parent.AddWindow(self.button1, 0, border=8, flag=wx.RIGHT)
        parent.AddWindow(self.button2, 0)
        parent.AddStretchSpacer(1)
        parent.AddWindow(self.forward, 0, border=5, flag=wx.RIGHT)

    def __init_sizers(self):
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)
        self.boxSizer2 = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.initCollBoxSizer1Items(self.boxSizer1)
        self.initCollBoxSizer2Items(self.boxSizer2)

    def __init_ctrls(self, prnt):
        wx.Dialog.__init__(self, id=wxID_EDITDIALOG, name=u'editDialog',
            parent=prnt, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
            title=_(u"Manually Edit"))
        self.SetIcon(wx.Icon(utils.icon_path(u'edit.png'), wx.BITMAP_TYPE_PNG))



        self.staticText1 = wx.StaticText(id=wxID_EDITDIALOGSTATICTEXT1,
            label=_(u"Manually edit name, use with care."),
            name='staticText1', parent=self)

        self.staticText2 = wx.StaticText(id=wxID_EDITDIALOGSTATICTEXT2,
            label=_(u"Use the up and down keys to save changes to the name and \nmove to another item."),
            name='staticText2', parent=self)

        self.staticText3 = wx.StaticText(id=wxID_EDITDIALOGSTATICTEXT3,
            label=_(u"Previewing will destroy any changes!"),
            name='staticText3', parent=self)
        self.staticText3.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL , wx.BOLD, False))

        self.value = wx.TextCtrl(id=wxID_EDITDIALOGVALUE, name=u'value',
            parent=self, size=wx.Size(410, -1), value=u'')

        self.backward = wx.Button(id=wx.ID_BACKWARD, name='backward', parent=self)
        self.backward.Bind(wx.EVT_BUTTON, self.setNextItemFromButton,
            id=wx.ID_BACKWARD)

        self.button1 = wx.Button(id=wx.ID_CANCEL, name='button1', parent=self)

        self.button2 = wx.Button(id=wx.ID_OK, name='button2', parent=self)

        self.forward = wx.Button(id=wx.ID_FORWARD, name='forward', parent=self)
        self.forward.Bind(wx.EVT_BUTTON, self.setNextItemFromButton,
            id=wx.ID_FORWARD)

        # Windows and Linux do things differently
        # Bind both ways to be sure
        self.value.Bind(wx.EVT_KEY_DOWN, self.keyboardEvents)
        self.Bind(wx.EVT_KEY_DOWN, self.keyboardEvents)

        self.__init_sizers()

    def __init__(self, parent, item):
        self.parent = parent
        self.__init_ctrls(parent)
        self.SetSizerAndFit(self.boxSizer1)

        # the dialog should appear just above the bottom window
        self.CentreOnParent()
        pos = self.GetPositionTuple()
        newY = self.GetScreenRect().height + 50
        self.MoveXY(pos[0], pos[1] - newY)

        self.loadItem(item)


    # load the item's value and apply it to the dialog
    def loadItem(self, item):
        new = self.parent.get_names(item)[1]
        self.value.SetValue(new[0])
        self.item = item
        self.parent.set_item_selected(self.item)
        self.value.SetFocus()
        self.value.SetInsertionPointEnd()

    # get the new name of the item
    def getValue(self):
        return self.value.GetValue()

    def setNewName(self):
        value = self.getValue()
        self.parent.set_name(self.item, value)

    # get the next item, adjust for begining and end of list
    def getNextItem(self, change):
        nextItem = self.item + change
        totalItems = self.parent.GetItemCount()
        if nextItem < 0:
            nextItem = totalItems - 1
        elif nextItem >= totalItems:
            nextItem = 0
        return nextItem

    # apply the new name to the item and move on to the next item
    def setValueAndContinue(self, nextItem):
        self.setNewName()
        self.parent.set_item_deselected(self.item)
        self.loadItem(nextItem)

    # get the next item based on button pressed
    def setNextItemFromButton(self, event):
        if event.GetId() == wx.ID_FORWARD:
            nextItem = self.getNextItem(1)
        else:
            nextItem = self.getNextItem(-1)
        self.setValueAndContinue(nextItem)

    # filter keyboard events
    def keyboardEvents(self, event):
        keyCode = event.GetKeyCode()

        if keyCode == wx.WXK_PAGEUP or keyCode == wx.WXK_UP:
            nextItem = self.getNextItem(-1)
            self.setValueAndContinue(nextItem)

        elif keyCode == wx.WXK_PAGEDOWN or keyCode == wx.WXK_DOWN:
            nextItem = self.getNextItem(1)
            self.setValueAndContinue(nextItem)

        elif keyCode == wx.WXK_RETURN:
            self.setNewName()
            self.Destroy()

        else:
            event.Skip()