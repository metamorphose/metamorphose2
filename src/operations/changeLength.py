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
from operation import Operation

[wxID_PANEL, wxID_PANELMOD_LENGTH, wxID_PANELMOD_LENGTH_DIRECTION,
 wxID_PANELMOD_LENGTH_PAD, wxID_PANELMOD_LENGTH_POSITION,
 wxID_PANELMOD_LENGTH_TYPE, wxID_PANELSTATICBOX1, wxID_PANELSTATICTEXT2,
 wxID_PANELSTATICTEXT3, wxID_PANELSTATICTEXT4, wxID_PANELSTATICTEXT5,
 wxID_PANELSTATICTEXT8, wxID_MAINPANELMOD_LENGTH
] = [wx.NewId() for __init_ctrls in range(13)]

class OpPanel(Operation):
    def __init_sizer(self):
        mainSizer = wx.StaticBoxSizer(self.staticBox1, wx.VERTICAL)
        rowA = wx.BoxSizer(wx.HORIZONTAL)
        rowA.Add(self.mod_length_type,0,wx.LEFT,5)
        rowA.Add(self.staticText2,0,wx.ALIGN_CENTRE|wx.LEFT,10)
        rowA.Add(self.mod_length,0,wx.LEFT,5)
        rowA.Add(self.staticText8,0,wx.ALIGN_CENTRE|wx.LEFT,5)
        rowA.Add(self.staticText4,0,wx.ALIGN_CENTRE|wx.LEFT,15)
        rowA.Add(self.mod_length_direction,0,wx.LEFT,5)

        rowB = wx.BoxSizer(wx.HORIZONTAL)
        rowB.Add(self.staticText3,0,wx.ALIGN_CENTRE|wx.LEFT,5)
        rowB.Add(self.mod_length_pad,0,wx.LEFT,5)
        rowB.Add(self.staticText5,0,wx.ALIGN_CENTRE|wx.LEFT,15)
        rowB.Add(self.mod_length_position,0,wx.LEFT,5)

        mainSizer.Add(rowA,0,wx.TOP,25)
        mainSizer.Add(rowB,0,wx.TOP|wx.BOTTOM,25)

        self.SetSizerAndFit(mainSizer)

    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_PANEL, name=u'changeLengthPanel', parent=prnt,
              pos=wx.Point(369, 293), size=wx.Size(524, 304),
              style=wx.TAB_TRAVERSAL)

        self.staticBox1 = wx.StaticBox(id=wxID_PANELSTATICBOX1,
              label=_(u"How to change the length:"), name='staticBox1',
              parent=self, pos=wx.Point(16, 16),
              style=0)

        self.mod_length_type = wx.Choice(choices=[_(u"Cut"), _(u"Pad"),
              _(u"Both")], id=wxID_PANELMOD_LENGTH_TYPE,
              name=u'mod_length_type', parent=self, pos=wx.Point(32, 64),)
        self.mod_length_type.SetSelection(0)
        self.mod_length_type.Bind(wx.EVT_CHOICE, self.__enable_options,
              id=wxID_PANELMOD_LENGTH_TYPE)

        self.mod_length = wx.SpinCtrl(id=wxID_MAINPANELMOD_LENGTH, initial=1,
              max=255, min=1, name=u'mod_length', parent=self, pos=wx.Point(120,
              64), size=wx.Size(50, -1), value='64',
              style=wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER)
        self.mod_length.SetValue(64)
        self.mod_length.SetToolTipString(_(u"Length after modification"))
        self.mod_length.Bind(wx.EVT_TEXT_ENTER, main.show_preview,
              id=wxID_MAINPANELMOD_LENGTH)
        self.mod_length.Bind(wx.EVT_SPINCTRL, main.show_preview,
              id=wxID_MAINPANELMOD_LENGTH)

        self.staticText8 = wx.StaticText(id=wxID_PANELSTATICTEXT8,
              label=_(u"characters,"), name=u'staticText8', parent=self,
              pos=wx.Point(192, 72), style=0)

        self.staticText2 = wx.StaticText(id=wxID_PANELSTATICTEXT2,
              label=_(u"to:"), name=u'staticText2', parent=self,
              pos=wx.Point(96, 64), style=0)

        self.staticText4 = wx.StaticText(id=wxID_PANELSTATICTEXT4,
              label=_(u"starting from the:"), name=u'staticText4', parent=self,
              pos=wx.Point(256, 72), style=0)

        self.mod_length_direction = wx.Choice(choices=[_(u"right"),
              _(u"left")], id=wxID_PANELMOD_LENGTH_DIRECTION,
              name=u'mod_length_direction', parent=self, pos=wx.Point(352, 64))
        self.mod_length_direction.SetSelection(0)
        self.mod_length_direction.Bind(wx.EVT_CHOICE, main.show_preview,
              id=wxID_PANELMOD_LENGTH_DIRECTION)

        self.staticText3 = wx.StaticText(id=wxID_PANELSTATICTEXT3,
              label=_(u"Character for padding:"), name=u'staticText3', parent=self,
              style=0,)
        self.staticText3.Enable(False)

        self.mod_length_pad = wx.TextCtrl(id=wxID_PANELMOD_LENGTH_PAD,
              name=u'mod_length_pad', parent=self,
              size=wx.Size(24, -1), style=0, value='0')
        self.mod_length_pad.SetMaxLength(1)
        self.mod_length_pad.Enable(False)
        self.mod_length_pad.Bind(wx.EVT_TEXT, main.show_preview)

        self.staticText5 = wx.StaticText(id=wxID_PANELSTATICTEXT5,
              label=_(u"Position for padding:"), name=u'staticText5', parent=self,
              pos=wx.Point(136, 112), style=0)
        self.staticText5.Enable(False)

        self.mod_length_position = wx.SpinCtrl(id=wxID_PANELMOD_LENGTH_POSITION,
              initial=0, max=256, min=-256, name=u'mod_length_position',
              parent=self, pos=wx.Point(200, 104), size=wx.Size(45, -1),
              value='0', style=wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER)
        self.mod_length_position.SetValue(0)
        self.mod_length_position.Enable(False)
        self.mod_length_position.SetToolTipString(_(u"(0 = first character)"))
        self.mod_length_position.Bind(wx.EVT_TEXT_ENTER, main.show_preview,
              id=wxID_PANELMOD_LENGTH_POSITION)
        self.mod_length_position.Bind(wx.EVT_SPINCTRL, main.show_preview,
              id=wxID_PANELMOD_LENGTH_POSITION)

    def __init__(self, parent, main_window, params={}):
        Operation.__init__(self, params)
        global main
        main = main_window
        self.__init_ctrls(parent)
        self.__init_sizer()

    def __enable_options(self, event):
        """Activate or disativate length modification options."""
        type = self.mod_length_type.GetSelection()
        padding = (self.mod_length_pad, self.staticText3, self.staticText5,
          self.mod_length_position)
        if (type == 1 or type == 2):
            for option in padding:
                option.Enable(True)
        else:
            for option in padding:
                option.Enable(False)
        main.show_preview(event)

    def on_config_load(self):
        """Update GUI elements, settings after config load."""
        self.__enable_options(False)

    def rename_item(self, path, name, ext, original):
        """Change length of name."""
        newName = self.joinExt(name,ext)
        if not newName:
            return path,name,ext

        type = self.mod_length_type.GetSelection()# 0 = cut, 1 = pad, 2 = both
        width = int(self.mod_length.GetValue())
        direction = self.mod_length_direction.GetSelection()# 0 = right, 1 = left
        position = self.mod_length_position.GetValue()
        padChar = self.mod_length_pad.GetValue()

        # helper functions called latter
        # truncating
        def truncate(newName):
            if direction == 1:#left
                cut = len(newName) - width
                if cut < 0: cut = 0
                newName = newName[cut:]
            else:
                newName = newName[:width]
            return newName
        # padding
        def pad(newName):
            if direction == 0 and position == 0 and padChar:
                newName = newName.ljust(width, padChar)
            elif direction == 1 and position == 0 and padChar:
                newName = newName.rjust(width, padChar)
            #padding by inserting at position:
            else:
                padSize = width - len(newName)
                newName = newName[:position] + unicode(padChar*padSize) +\
                               newName[position:]
            return newName

        # perform requested operation:
        if type == 0:#cut
            newName = truncate(newName)
        elif type == 1:#pad
            newName = pad(newName)
        elif type == 2:#both
            if len(newName) < width:
                newName = pad(newName)
            elif len(newName) > width:
                newName = truncate(newName)

        # apply to name and/or ext
        name,ext = self.splitExt(newName,name,ext)

        return path, name, ext
