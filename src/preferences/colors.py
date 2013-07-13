# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2013 ianaré sévi <ianare@gmail.com>
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

class ColourPickerCtrl(wx.ColourPickerCtrl):
    """Custom wx.ColourPickerCtrl to make changing look easier."""
    def __init__(self, parent, col, name):
        wx.ColourPickerCtrl.__init__(self, parent=parent, id=-1, col=col,
									 name=name, style=wx.CLRP_USE_TEXTCTRL)
        self.SetMinSize(wx.Size(250, 35))
        self.SetPickerCtrlProportion(1)
        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.choose_color, self)

    def SetColour(self, colname):
        wx.ColourPickerCtrl.SetColour(self, colname)
        self.choose_color(True)

    def choose_color(self, event):
        value = self.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
        self.GetTextCtrl().SetValue(value)


class Panel(wx.Panel):
    """Color preferences panel."""

    def __init_renamecolor_sizer(self, parent):
        
        parent.AddWindow(self.willChangeColorTxt, 0,
						 flag=wx.ALIGN_CENTER_VERTICAL, border=0)
        parent.AddWindow(self.willChangeColor, 0, flag=0, border=0)

        parent.AddWindow(self.renamedColorTxt, 0,
						 flag=wx.ALIGN_CENTER_VERTICAL, border=0)
        parent.AddWindow(self.renamedColor, 0, flag=0, border=0)


        parent.AddWindow(self.errorColorTxt, 0,
						 flag=wx.ALIGN_CENTER_VERTICAL, border=0)
        parent.AddWindow(self.errorColor, 0, 0, border=0)

        parent.AddWindow(self.warnColorTxt, 0,
						 flag=wx.ALIGN_CENTER_VERTICAL, border=0)
        parent.AddWindow(self.warnColor, 0, 0, border=0)

    def __init_sizers(self):
        self.renameColorSizer = wx.FlexGridSizer(4, 2, 6, 8)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.__init_renamecolor_sizer(self.renameColorSizer)

        self.mainSizer.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        self.mainSizer.AddSizer(self.renameColorSizer, 0,
								flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=10)
        self.mainSizer.AddWindow(self.setDefaultsBtn, 0,
								 flag=wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
        self.SetSizer(self.mainSizer)

    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, name=u'Colors', parent=prnt, style=wx.TAB_TRAVERSAL)

        self.willChangeColorTxt = wx.StaticText(self, id=-1, label=_(u"Will be renamed"))
        self.willChangeColor = ColourPickerCtrl(self, col='#E5FFE5', name="willChangeColor")
        self.willChangeColor.SetToolTipString(_(u"Color of items to be renamed."))

        self.renamedColorTxt = wx.StaticText(self, id=-1, label=_(u"Successfully renamed"))
        self.renamedColor = ColourPickerCtrl(self, col='#97F27F', name="renamedColor")
        self.renamedColor.SetToolTipString(_(u"Color of successfully renamed items."))

        self.errorColorTxt = wx.StaticText(self, -1, label=_(u"Error"))
        self.errorColor = ColourPickerCtrl(self, col='#FF1616', name="errorColor")
        self.errorColor.SetToolTipString(_(u"Color of items with errors."))

        self.warnColorTxt = wx.StaticText(self, -1, label=_(u"Warning"))
        self.warnColor = ColourPickerCtrl(self, col='#FDEB22', name="warnColor")
        self.warnColor.SetToolTipString(_(u"Color of items with warnings."))

        self.setDefaultsBtn = wx.Button(self, -1, label=_(u"Set colors to defaults"),
										name=u'setDefaultsBtn')
        self.Bind(wx.EVT_BUTTON, self.set_defaults, self.setDefaultsBtn)

        self.__init_sizers()

    def __init__(self, parent):
        self.__init_ctrls(parent)
        self.SetSizerAndFit(self.mainSizer)

    def set_defaults(self, event):
        defaults = {
            'renamedColor': '#97F27F',
            'willChangeColor': '#E5FFE5',
            'errorColor': '#FF1616',
            'warnColor': '#FDEB22',
        }
        for name, value in defaults.items():
            clrCtrl = getattr(self, name)
            clrCtrl.SetColour(value)
