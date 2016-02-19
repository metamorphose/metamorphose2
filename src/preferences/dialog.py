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

from __future__ import print_function
import logging

import app
import automation
import colors
import display
import errorCheck
import general
import utils
import wx


class Notebook(wx.Toolbook):
    """
    Notebook for preferences.
    """
    def __init__(self, parent, id, name):
        wx.Toolbook.__init__(self, parent, id, name=name, style=wx.BK_TOP)

        il = wx.ImageList(22, 22)
        imgGeneral = il.Add(wx.Bitmap(utils.icon_path(u'22/general.png'), wx.BITMAP_TYPE_PNG))
        imgDisplay = il.Add(wx.Bitmap(utils.icon_path(u'22/display.png'), wx.BITMAP_TYPE_PNG))
        imgColors = il.Add(wx.Bitmap(utils.icon_path(u'22/colors.png'), wx.BITMAP_TYPE_PNG))
        imgAuto = il.Add(wx.Bitmap(utils.icon_path(u'22/auto.png'), wx.BITMAP_TYPE_PNG))
        imgLog = il.Add(wx.Bitmap(utils.icon_path(u'22/log.png'), wx.BITMAP_TYPE_PNG))
        imgError = il.Add(wx.Bitmap(utils.icon_path(u'22/error.png'), wx.BITMAP_TYPE_PNG))
        self.AssignImageList(il)

        panels = (
                  (general, _(u'General'), imgGeneral),
                  (display, _(u'Display'), imgDisplay),
                  (colors, _(u'Colors'), imgColors),
                  (automation, _(u'Automate'), imgAuto),
                  (logging, _(u'Logging'), imgLog),
                  (errorCheck, _(u'Error Checks'), imgError)
                  )
        i = 0
        for pane in panels:
            page = getattr(pane[0], 'Panel')
            page = page(self)
            self.AddPage(page, pane[1], imageId=pane[2])
            notebookPage = self.GetPage(i)
            parent.load_prefs(notebookPage)
            if hasattr(notebookPage, 'init_enabled'):
                notebookPage.init_enabled()
            i += 1


class Dialog(wx.Dialog):
    """
    Preferences dialog.
    """
    def __init_mainsizer_items(self, parent):
        parent.AddWindow(self.notebook, 1, border=5,
                         flag=wx.ALL | wx.EXPAND)
        parent.AddSizer(self.buttons, 0, border=5, flag=wx.ALL | wx.EXPAND)

    def __init_buttons_items(self, parent):
        parent.AddSpacer((110, -1), 0, border=0, flag=0)
        parent.AddWindow(self.apply, 0, border=25, flag=wx.RIGHT)
        parent.AddWindow(self.ok, 0, border=108, flag=wx.RIGHT)
        parent.AddSpacer((10, -1), 1, border=0, flag=0)
        parent.AddWindow(self.close, 0, border=0, flag=0)

    def __init_sizers(self):
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.buttons = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.__init_mainsizer_items(self.mainSizer)
        self.__init_buttons_items(self.buttons)
        utils.set_min_size(self, ignoreClasses=(
                           wx.TextCtrl, wx.Button, wx.Choice, wx.SpinCtrl,
                           wx.FilePickerCtrl, wx.DirPickerCtrl, wx.ColourPickerCtrl))
        self.SetSizerAndFit(self.mainSizer)

    def __init_ctrls(self, parent):
        wx.Dialog.__init__(self, name=u'dialog', parent=parent,
                           style=wx.CAPTION | wx.STAY_ON_TOP, title=_(u"Preferences"))
        self.SetIcon(wx.Icon(utils.icon_path(u'preferences.ico'),
                     wx.BITMAP_TYPE_ICO))

        self.apply = wx.Button(id=wx.ID_APPLY, name=u'apply', parent=self, style=0)
        self.apply.Bind(wx.EVT_BUTTON, self.__on_apply_button)

        self.ok = wx.Button(id=wx.ID_OK, name=u'ok', parent=self, style=0)
        self.ok.SetDefault()
        self.ok.Bind(wx.EVT_BUTTON, self.__on_ok_button)

        self.close = wx.Button(id=wx.ID_CANCEL, name=u'close', parent=self, style=0)
        self.close.Bind(wx.EVT_BUTTON, self.__close_diag)

        self.notebook = Notebook(id=-1, name=u'notebook', parent=self)

        self.__init_sizers()

    def __init__(self, parent, methods, initial):
        app.debug_print("Open preferences dialog")
        global main
        main = parent
        self.prefs = methods
        self.__init_ctrls(parent)

        self.CentreOnScreen()
        # to see if these change when applying
        self.oldDirTree = self.prefs.get(u'useDirTree')
        self.oldSHowHiddenDirs = self.prefs.get(u'showHiddenDirs')

    def __on_apply_button(self, event):
        app.debug_print("Save preferences from dialog")
        self.prefs.set_prefs(self)
        prefs = app.prefs = self.prefs
        if prefs.get(u'useDirTree') != self.oldDirTree:
            main.picker.set_tree()
        if prefs.get(u'showHiddenDirs') != self.oldSHowHiddenDirs:
            main.picker.dirPicker.ShowHidden(prefs.get(u'showHiddenDirs'))
        self.oldDirTree = prefs.get(u'useDirTree')
        self.oldSHowHiddenDirs = prefs.get(u'showHiddenDirs')
        main.bottomWindow.display.set_preferences()
        main.show_preview(True)

    def load_prefs(self, panel):
        """
        load preferences from file and apply them to a panel.
        """
        app.debug_print('Load preferences from file into %s' % panel.GetName())
        object_types = (
            wx.CheckBox,
            wx.RadioButton,
            wx.SpinCtrl,
            wx.ComboBox,
            wx.TextCtrl,
            wx.Choice,
            wx.DirPickerCtrl,
            wx.FilePickerCtrl,
            wx.ColourPickerCtrl
            )
        for child in panel.GetChildren():
            if not isinstance(child, object_types):
                continue
            child_name = child.GetName()
            try:
                v = self.prefs.get(child_name)
            except KeyError:
                app.debug_print("Could not find value for: '%s'" % (child_name))
                # forces the user to apply prefs, hopefully fixing the file
                self.close.Enable(False)
            else:
                app.debug_print("   %s = %s" % (child_name, v))
                if isinstance(child, wx.CheckBox) or isinstance(child, wx.RadioButton)\
                    or isinstance(child, wx.SpinCtrl):
                        child.SetValue(v)
                elif isinstance(child, wx.ComboBox) or isinstance(child, wx.TextCtrl):
                    child.SetValue(unicode(v))
                elif isinstance(child, wx.Choice):
                    child.SetSelection(v)
                elif isinstance(child, wx.DirPickerCtrl) or isinstance(child, wx.FilePickerCtrl):
                    child.SetPath(unicode(v))
                elif isinstance(child, wx.ColourPickerCtrl):
                    child.SetColour(v)

    def __close_diag(self, event):
        self.Destroy()

    def __on_ok_button(self, event):
        self.__on_apply_button(event)
        self.Destroy()
