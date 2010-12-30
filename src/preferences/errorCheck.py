# -*- coding: utf-8 -*-
#
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

"""Error checking preferences panel."""

import wx
import platform

[wxID_PANEL, wxID_PANELDELETEBADCHARS,
 wxID_PANELMARKBADCHARS, wxID_PANELMARKWARNING, wxID_PANELUSEWINCHARS,
 wxID_PANELUSEWINNAMES, wxID_PANELWINNAMESBAD, wxID_PANELWINNAMESWARN,
] = [wx.NewId() for __init_ctrls in range(8)]

class Panel(wx.Panel):
    def __init_sizers(self):
        self.itemSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.__init_itemsizer_items(self.itemSizer)
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.AddSizer(self.itemSizer, 0, border=10,
            flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALL)
        self.SetSizer(self.mainSizer)

    def __init_itemsizer_items(self, parent):
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.useWinChars, 0, border=15, flag=wx.LEFT)
        parent.AddSpacer(wx.Size(8, 4), border=0, flag=0)
        parent.AddWindow(self.markWarning, 0, border=38, flag=wx.LEFT)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.markBadChars, 0, border=38, flag=wx.LEFT)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.deleteBadChars, 0, border=38, flag=wx.LEFT)
        parent.AddSpacer(wx.Size(8, 16), border=0, flag=0)
        parent.AddWindow(self.useWinNames, 0, border=15, flag=wx.LEFT)
        parent.AddSpacer(wx.Size(8, 4), border=0, flag=0)
        parent.AddWindow(self.winNamesWarn, 0, border=38, flag=wx.LEFT)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.winNamesBad, 0, border=38, flag=wx.LEFT)
        parent.AddSpacer(wx.Size(8, 16), border=0, flag=0)

    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_PANEL, name=u'ErrorCheck', parent=prnt,
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(312, 277))

        self.useWinChars = wx.CheckBox(id=wxID_PANELUSEWINCHARS,
              label=_(u'Use Windows compatible characters'),
              name=u'useWinChars', parent=self)
        self.useWinChars.SetValue(True)
        self.useWinChars.Bind(wx.EVT_CHECKBOX, self.allow_winchars,
              id=wxID_PANELUSEWINCHARS)

        self.markWarning = wx.RadioButton(id=wxID_PANELMARKWARNING,
              label=_(u'Mark name as warning'), name=u'markWarning',
              parent=self, style=wx.RB_GROUP)
        self.markWarning.Enable(False)

        self.markBadChars = wx.RadioButton(id=wxID_PANELMARKBADCHARS,
              label=_(u'Mark name as bad'), name=u'markBadChars', parent=self)

        self.deleteBadChars = wx.RadioButton(id=wxID_PANELDELETEBADCHARS,
              label=_(u'Fix names (remove bad characters)'),
              name=u'deleteBadChars', parent=self)

        self.useWinNames = wx.CheckBox(id=wxID_PANELUSEWINNAMES,
              label=_(u'Use Windows compatible names'), name=u'useWinNames',
              parent=self)
        self.useWinNames.SetHelpText(u'')
        self.useWinNames.Bind(wx.EVT_CHECKBOX, self.allow_winnames,
              id=wxID_PANELUSEWINNAMES)

        self.winNamesWarn = wx.RadioButton(id=wxID_PANELWINNAMESWARN,
              label=_(u'Mark name as warning'), name=u'winNamesWarn',
              parent=self, style=wx.RB_GROUP)
        self.winNamesWarn.Enable(False)

        self.winNamesBad = wx.RadioButton(id=wxID_PANELWINNAMESBAD,
              label=_(u'Mark name as bad'), name=u'winNamesBad', parent=self)

        self.__init_sizers()


    def __init__(self, parent):
        self.__init_ctrls(parent)

        # Default preferences:
        if platform.system() != 'Windows':
            self.winNamesWarn.SetValue(False)
            self.markWarning.SetValue(True)
        else:
            self.useWinNames.SetValue(True)
            self.winNamesBad.SetValue(True)
            self.deleteBadChars.SetValue(True)

    def init_enabled(self):
        """Enable or disable options."""
        self.allow_winchars(1)
        self.allow_winnames(1)

    def allow_winchars(self, event):
        """Enable or disable windows compatible characters options."""
        if self.useWinChars.GetValue():
            allow = True
        else:
            allow = False

        widgets = [self.markBadChars,self.deleteBadChars]
        if platform.system() != 'Windows':
            widgets.append(self.markWarning)

        for i in widgets:
            i.Enable(allow)

    def allow_winnames(self, event):
        """Enable or disable windows compatible names options."""
        if self.useWinNames.GetValue():
            allow = True
        else:
            allow = False

        widgets = [self.winNamesBad]
        if platform.system() != 'Windows':
            widgets.append(self.winNamesWarn)

        for i in widgets:
            i.Enable(allow)
