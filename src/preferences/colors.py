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
import utils

class Panel(wx.Panel):
    """Color preferences panel."""

    def __init_renamecolor_sizer(self, parent):
        parent.AddWindow(self.willChangeColorTxt, 0,
            flag=wx.ALIGN_CENTER_VERTICAL, border=0)
        parent.AddWindow(self.willChangeColor, 0, 0, border=0)
        parent.AddWindow(self.willChangeColorBtn, 0, 0, border=0)
        parent.AddWindow(self.renamedColorTxt, 0,
            flag=wx.ALIGN_CENTER_VERTICAL, border=0)
        parent.AddWindow(self.renamedColor, 0, 0, border=0)
        parent.AddWindow(self.renamedColorBtn, 0, 0, border=0)
        parent.AddWindow(self.errorColorTxt, 0,
            flag=wx.ALIGN_CENTER_VERTICAL, border=0)
        parent.AddWindow(self.errorColor, 0, 0, border=0)
        parent.AddWindow(self.errorColorBtn, 0, 0, border=0)
        parent.AddWindow(self.warnColorTxt, 0,
            flag=wx.ALIGN_CENTER_VERTICAL, border=0)
        parent.AddWindow(self.warnColor, 0, 0, border=0)
        parent.AddWindow(self.warnColorBtn, 0, 0, border=0)

    def __init_sizers(self):
        self.renameColorSizer = wx.FlexGridSizer(4, 3, 6, 8)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.__init_renamecolor_sizer(self.renameColorSizer)

        self.mainSizer.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        self.mainSizer.AddWindow(self.renameColorSizer, 0,
            flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, border=10)
        self.mainSizer.AddWindow(self.setDefaultsBtn, 0,
            flag=wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, border=5)
        self.SetSizer(self.mainSizer)

    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, name=u'Colors', parent=prnt, style=wx.TAB_TRAVERSAL)

        self.willChangeColorTxt = wx.StaticText(self, id=-1, label=_(u"Will be renamed"))

        self.willChangeColor = wx.TextCtrl(self, id=-1, size=wx.Size(100, -1),
            name=u'willChangeColor', value=u'#E5FFE5')
        self.willChangeColor.Enable(False)
        self.willChangeColor.SetToolTipString(_(u"Color of items to be renamed."))

        self.willChangeColorBtn = wx.Button(self, -1, label=_(u"Choose ..."),
            name=u'willChangeColorBtn')
        self.Bind(wx.EVT_BUTTON, self.choose_color, self.willChangeColorBtn)

        self.renamedColorTxt = wx.StaticText(self, id=-1, label=_(u"Successfully renamed"))

        self.renamedColor = wx.TextCtrl(self, id=-1, size=wx.Size(100, -1),
            value=u'#97F27F', name=u'renamedColor')
        self.renamedColor.Enable(False)
        self.renamedColor.SetToolTipString(_(u"Color of successfully renamed items."))

        self.renamedColorBtn = wx.Button(self, -1, label=_(u"Choose ..."),
            name=u'renamedColorBtn')
        self.Bind(wx.EVT_BUTTON, self.choose_color, self.renamedColorBtn)
        
        self.errorColorTxt = wx.StaticText(self, -1, label=_(u"Error"))

        self.errorColor = wx.TextCtrl(self, -1, size=wx.Size(100, -1),
            name=u'errorColor', value=u'#FF1616')
        self.errorColor.Enable(False)
        self.errorColor.SetToolTipString(_(u"Color of items with errors."))

        self.errorColorBtn = wx.Button(self, -1, label=_(u"Choose ..."),
            name=u'errorColorBtn')
        self.Bind(wx.EVT_BUTTON, self.choose_color, self.errorColorBtn)
        
        self.warnColorTxt = wx.StaticText(self, -1, label=_(u"Warning"))

        self.warnColor = wx.TextCtrl(self, -1, size=wx.Size(100, -1),
            name=u'warnColor', value=u'#FDEB22')
        self.warnColor.Enable(False)
        self.warnColor.SetToolTipString(_(u"Color of items with warnings."))

        self.warnColorBtn = wx.Button(self, -1, label=_(u"Choose ..."),
            name=u'warnColorBtn')
        self.Bind(wx.EVT_BUTTON, self.choose_color, self.warnColorBtn)

        self.setDefaultsBtn = wx.Button(self, -1, label=_(u"Set colors to defaults"),
            name=u'setDefaultsBtn')
        self.Bind(wx.EVT_BUTTON, self.set_defaults, self.setDefaultsBtn)

        self.__init_sizers()

    def __init__(self, parent):
        self.__init_ctrls(parent)
        self.SetSizerAndFit(self.mainSizer)

    def init_enabled(self):
        textCtrls = (
            'renamedColor', 'willChangeColor',
            'errorColor', 'warnColor'
        )
        for name in textCtrls:
            textCtrl = getattr(self, name)
            value = textCtrl.GetValue()
            textCtrl.SetBackgroundColour(value)

    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        try:
            rgb = tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))
        except ValueError:
            msg = _(u"Invalid color specified.")
            title = _(u"Error")
            utils.make_err_msg(msg, title)
            return False
        else:
            return rgb

    def set_defaults(self, event):
        defaults = {
            'renamedColor' : '#97F27F',
            'willChangeColor' : '#E5FFE5',
            'errorColor' : '#FF1616',
            'warnColor' : '#FDEB22',
        }
        for name, value in defaults.items():
            textCtrl = getattr(self, name)
            textCtrl.SetValue(value)
            textCtrl.SetBackgroundColour(value)

    def choose_color(self, event):
        name = event.GetEventObject().GetName()[:-3]
        textCtrl = getattr(self, name)
        value = textCtrl.GetValue()
        value = self.hex_to_rgb(value)
        
        colorData = wx.ColourData()
        colorData.SetChooseFull(False)
        colorData.SetColour(value)
        colorDialog = wx.ColourDialog(self, colorData)
        colorDialog.ShowModal()
        colorData = colorDialog.GetColourData()
        color = colorData.GetColour()
        #if color[0] != -1:
        color = color.GetAsString(wx.C2S_HTML_SYNTAX)
        #else:
        #    color = app.prefs[name]
        textCtrl.SetValue(color)
        textCtrl.SetBackgroundColour(color)
        
