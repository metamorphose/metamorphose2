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

import re
import sre_constants

import wx

[wxID_PANEL, wxID_PANELA_Z, wxID_PANELDIGIT,
    wxID_PANELREG_EXPR, wxID_PANELREG_EXP_DIV,
    wxID_PANELREG_EXP_I, wxID_PANELREG_EXP_U,
] = [wx.NewId() for __init_ctrls in range(7)]

class Panel(wx.Panel):
    """Panel to hold regular expression stuff."""
    
    def __init_sizer(self):
        regExprSizer = wx.BoxSizer(wx.HORIZONTAL)
        regExprSizer.Add(self.regExpr, 0, wx.ALIGN_CENTER | wx.RIGHT, 3)
        regExprSizer.Add(self.iRegExpr, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 3)
        regExprSizer.Add(self.uRegExpr, 0, wx.ALIGN_CENTER)
        regExprSizer.Add((0, 0), 1)
        regExprSizer.Add(self.regExpDiv, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 3)
        regExprSizer.Add((0, 0), 1)
        regExprSizer.Add(self.aToZ, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        regExprSizer.Add(self.digit, 0, wx.ALIGN_CENTER)
        regExprSizer.Add((0, 0), 60)
        self.SetSizerAndFit(regExprSizer)
        #mainSizer.Add(regExprSizer,0,wx.EXPAND|wx.TOP,5)

    def __init_ctrls(self, prnt, name):
        wx.Panel.__init__(self, id=wxID_PANEL, name=name, parent=prnt,
                          style=wx.TAB_TRAVERSAL)

        self.regExpr = wx.CheckBox(id=wxID_PANELREG_EXPR,
                                   label=_(u"Evaluate as regular expression"), name=u'regExpr', parent=self,
                                   style=0)
        self.regExpr.SetValue(False)
        self.regExpr.Bind(wx.EVT_CHECKBOX, prnt.activate_options,
                          id=wxID_PANELREG_EXPR)

        self.iRegExpr = wx.CheckBox(id=wxID_PANELREG_EXP_I, label=_(u"case sensitive"),
                                    name=u'iRegExpr', parent=self)
        self.iRegExpr.SetValue(False)
        self.iRegExpr.SetToolTipString(_(u"Differentiate between upper and lower case"))
        self.iRegExpr.Enable(False)
        self.iRegExpr.Bind(wx.EVT_CHECKBOX, prnt.define_regex)

        self.uRegExpr = wx.CheckBox(id=wxID_PANELREG_EXP_U, label=_(u"Unicode"),
                                    name=u'uRegExpr', parent=self)
        self.uRegExpr.SetValue(True)
        self.uRegExpr.SetToolTipString(_(u"Unicode match (\w matches 'a','b','c', etc)"))
        self.uRegExpr.Enable(False)
        self.uRegExpr.Bind(wx.EVT_CHECKBOX, prnt.define_regex)

        self.regExpDiv = wx.StaticLine(id=wxID_PANELREG_EXP_DIV,
                                       name=u'regExpDiv', parent=self, size=wx.Size(2, 21),
                                       style=wx.LI_VERTICAL)

        self.aToZ = wx.Button(id=wxID_PANELA_Z, label=_(u"[a-z]"), name=u'aToZ',
                              parent=self, style=wx.BU_EXACTFIT)
        self.aToZ.SetToolTipString(_(u"All alphabetical characters"))
        self.aToZ.Enable(False)
        self.aToZ.Bind(wx.EVT_BUTTON, self._add_regex_buttons)

        self.digit = wx.Button(id=wxID_PANELDIGIT, label=_(u"[0-9]"),
                               name=u'digit', parent=self, style=wx.BU_EXACTFIT)
        self.digit.SetToolTipString(_(u"All number characters"))
        self.digit.Enable(False)
        self.digit.Bind(wx.EVT_BUTTON, self._add_regex_buttons)

    def __init__(self, parent, main_window, name=u'regExpPanel'):
        global main
        main = main_window
        self.parent = parent
        self.__init_ctrls(parent, name)
        self.__init_sizer()

    def _add_regex_buttons(self, event):
        """Add some predefined REs."""
        if event.GetId() == wxID_PANELA_Z:
            txt = "[^\W\d]"
        elif event.GetId() == wxID_PANELDIGIT:
            txt = "\d"
        activatedField = self.activatedField

        iPoint = activatedField.GetInsertionPoint()
        activatedField.WriteText(txt)
        activatedField.SetFocus()
        activatedField.SetInsertionPoint(iPoint + len(txt))

    def set_active(self, activate):
        """Set active widgets."""
        reg_exp_tup = (self.iRegExpr, self.uRegExpr,
                       self.aToZ, self.digit)
        for option in reg_exp_tup:
            option.Enable(activate)

    def set_activated_field(self, event):
        """Find focused text field."""
        self.activatedField = event.GetEventObject()

    def create_regex(self, REfind):
        """Compile regular expression."""
        self.parent.REmsg = False
        caseSensitive = self.iRegExpr.GetValue()
        useUnicode = self.uRegExpr.GetValue()
        try:
            # compile according to options
            if not caseSensitive and useUnicode:
                mod = re.compile(REfind, re.IGNORECASE | re.UNICODE)
            elif not caseSensitive:
                mod = re.compile(REfind, re.IGNORECASE)
            elif useUnicode:
                mod = re.compile(REfind, re.UNICODE)
            else:
                mod = re.compile(REfind)
        except sre_constants.error as err:
            mod = re.compile(r'')

            # give user a descriptive error message
            # set message directly for when items are NOT loaded
            main.set_status_msg(_(u"Regular-Expression: %s") % err, u'warn')

            # set message in variable for when items ARE loaded
            self.parent.REmsg = _(u"Regular-Expression: %s") % err

            # so we know not to change status text after re error msg
            app.REmsg = True
            pass
        else:
            # reset status message for when items are not loaded
            main.set_status_msg("", u'eyes')
            return mod
