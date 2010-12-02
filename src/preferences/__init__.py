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

from __future__ import print_function
import wx
import os
import codecs
import utils
import general
import automation
import display
import errorCheck
import logging

def create_dialog(parent, initial=False):
    """Create and return the preferences dialog."""
    return Dialog(parent,initial)

[wxID_DIALOG, wxID_DIALOGAPPLY, wxID_DIALOGCLOSE, wxID_DIALOGNOTEBOOK,
 wxID_DIALOGOK,
] = [wx.NewId() for __init_ctrls in range(5)]

class Methods:
    """
    Preference methods.
    """
    def __init__(self, MainWindow=False):
        global main
        main = MainWindow
        self.header = u'Version=%s\n'%main.version
        self.prefs = False

    def _find_pref_file(self):
        prefFile = utils.get_user_path(u'preferences.ini')
        return prefFile
    
    def _open_pref_file(self,type):
        prefFile = self._find_pref_file()
        utils.debug_print(main, "Opening as '%s' : %s"%(type,prefFile))
        prefFile = codecs.open(prefFile,type, 'utf-8')
        return prefFile

    def _create_new(self):
        """Create default preferences file."""
        prefFile = self._open_pref_file('w+')
        msg = _(u"Please take a moment to set your preferences.\n\n")
        title = _(u"Preferences")
        dlg = wx.MessageDialog(None, msg, title, wx.CAPTION|wx.OK|wx.ICON_EXCLAMATION)
        dlg.ShowModal()
        dlg.Destroy()
        # show preferences
        prefDiag = Dialog(main, initial=True)
        prefDiag.ShowModal()
        prefDiag.Destroy()

    def _load_preferences(self):
        """Get values from file (one way or another)"""
        prefFile = self._find_pref_file()
        # make sure the file exist and is filled:
        if not os.path.exists(prefFile) or os.path.getsize(prefFile) < 5:
            prefs = self._create_new()
        else:
            prefFile = self._open_pref_file('r')
            prefFile.seek(0)
            version = prefFile.readline().strip()[8:]
            # preferences are from prior version, create new file
            if version[:4] != main.version[:4]:
                prefs = self._create_new()
            else:
                prefs = self.read_file(prefFile)
        # use windows-compatible filenames?
        if prefs[u'useWinChars']:
            prefs[u'bad_chars'] = (u'\\',u'/',u':',u'*',u'?',u'"',u'>',u'<',u'|')

        if prefs[u'useWinNames']:
            prefs[u'bad_win_words'] = (u'con', u'prn', u'aux', u'clock$',
              u'nul', u'com1', u'com2', u'com3', u'com4', u'com5', u'com6', u'com7',
              u'com8', u'com9', u'lpt1', u'lpt2', u'lpt3', u'lpt4', u'lpt5',u'lpt6',
              u'lpt7', u'lpt8', u'lpt9')
        self.prefs = prefs
        
    def set_prefs(self, prefDialog):
        """Get values from panels and set to file."""
        prefFile = self._open_pref_file('w')
        options = self.header
        # get all pages in notebook
        for i in range(prefDialog.notebook.GetPageCount()):
            # section header is page name
            options += u'\n[%s]\n'%prefDialog.notebook.GetPageText(i)

            # get all controls in page
            for child in prefDialog.notebook.GetPage(i).GetChildren():
                value = None
                # order of instance checks is important
                if isinstance(child, wx.CheckBox):
                    value = int(child.GetValue())
                    type = 'CheckBox'
                elif isinstance(child, wx.RadioButton):
                    value = int(child.GetValue())
                    type = 'RadioButton'
                elif isinstance(child, wx.TextCtrl):
                    value = child.GetValue()
                    type = 'TextCtrl'
                elif isinstance(child, wx.SpinCtrl):
                    value = child.GetValue()
                    type = 'SpinCtrl'
                elif isinstance(child, wx.ComboBox):
                    value = child.GetValue()
                    type = 'ComboBox'
                elif isinstance(child, wx.Choice):
                    value = int(child.GetSelection())
                    type = 'Choice'
                
                if value is not None:
                    name = child.GetName()
                    options += u'%s=%s\n'%(name,value)
                    utils.debug_print(main, "%s (%s) = %s"%(name,type,value))
        prefFile.write(options)
        return self.read_file(prefFile)

    def read_file(self, prefFile):
        """Process file and assign results to prefs dictionary."""
        prefFile.seek(0)
        prefs = {}
        for line in prefFile:
            if line.find('=') > 0:
                line = line.replace(u'\n','')
                split = line.split('=')
                try:
                    prefs[split[0]] = int(split[1])
                except KeyError:
                    pass
                except ValueError:
                    prefs[split[0]] = unicode(split[1])
                    pass
        return prefs

    def get(self, preference, strict=True):
        """Attempt to load a preference setting, recreate pref file if needed."""
        if not self.prefs:
            self._load_preferences()
        try:
            return self.prefs[preference]
        except KeyError:
            if not strict:
                pass
            else:
                msg = _(u"\nThe preferences file is outdated or corrupt.")
                msg += _(u"\nWill now recreate the preferences file.")
                utils.make_err_msg(msg, _(u"Problem with preferences"))
                self._create_new()
                self._load_preferences()
                return self.get(preference)


class Dialog(wx.Dialog):
    """
    Preferences dialog.
    """
    def __init_mainsizer_items(self, parent):
        parent.AddWindow(self.notebook, 1, border=5,
              flag=wx.ALL | wx.EXPAND)
        parent.AddSizer(self.buttons, 0, border=5, flag=wx.ALL | wx.EXPAND)

    def __init_buttons_items(self, parent):
        parent.AddWindow(self.apply, 0, border=20, flag=wx.RIGHT)
        parent.AddWindow(self.ok, 0, border=105, flag=wx.RIGHT)
        parent.AddSpacer((10,8), 1, border=0, flag=0)
        parent.AddWindow(self.close, 0, border=0, flag=0)

    def __init_sizers(self):
        # generated method, don't edit
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.buttons = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.__init_mainsizer_items(self.mainSizer)
        self.__init_buttons_items(self.buttons)

        self.SetSizer(self.mainSizer)

    def __init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG, name=u'dialog', parent=prnt,
              style=wx.CAPTION | wx.RESIZE_BORDER, title=u'Preferences')

        self.notebook = wx.Notebook(id=wxID_DIALOGNOTEBOOK, name=u'notebook',
              parent=self, pos=wx.Point(5, 5), size=wx.Size(590, 40), style=0)

        self.apply = wx.Button(id=wx.ID_APPLY, name=u'apply', parent=self, style=0)
        self.apply.Bind(wx.EVT_BUTTON, self._on_apply_button)

        self.ok = wx.Button(id=wx.ID_OK, name=u'ok', parent=self, style=0)
        self.ok.Bind(wx.EVT_BUTTON, self._on_ok_button)

        self.close = wx.Button(id=wx.ID_CANCEL, name=u'close', parent=self, style=0)
        self.close.Bind(wx.EVT_BUTTON, self._close_diag)

        self.__init_sizers()

    def __init__(self, parent, initial):
        global main
        main = parent
        self.initial = initial
        self.__init_ctrls(parent)
        self.SetIcon(wx.Icon(utils.icon_path(u'preferences.ico'),
                     wx.BITMAP_TYPE_ICO))
        self.notebook.SetBackgroundColour(self.notebook.GetThemeBackgroundColour())

        self.prefMethods = Methods(main)
        if not initial:
            prefs = self.prefMethods
        else:
            self.close.Enable(False)
            self.apply.Enable(False)

        # the panels to add to the notebook
        self.panels = ((general,_(u'General')),
                       (display, _(u'Display')),
                       (automation, _(u'Automate')),
                       (logging, _(u'Logging')),
                       (errorCheck, _(u'Error Checks')))
        # add panel to notebook
        i = 0
        for pane in self.panels:
            page = getattr(pane[0], 'Panel')
            self.notebook.AddPage(page(self.notebook), pane[1])
            notebookPage = self.notebook.GetPage(i)
            if not initial:
                self._load_prefs(notebookPage, prefs)
            if hasattr(notebookPage, 'init_enabled'):
                notebookPage.init_enabled()
            i += 1

        #utils.set_min_size(self)
        utils.set_min_size(self,ignoreClasses=(wx.TextCtrl,wx.Button,wx.Choice,
                                               wx.SpinCtrl))
        # set the window size
        self.Fit()
        self.CentreOnScreen()

        # to see if these change when applying
        if not initial:
            self.oldDirTree = prefs.get(u'useDirTree')
            self.oldSHowHiddenDirs = prefs.get(u'showHiddenDirs')

    def _on_apply_button(self, event):
        self.prefMethods.set_prefs(self)
        prefs = main.prefs = self.prefMethods

        #if self.prefs.get(u'autoPreviewPicker'):
        #    self.OnPreviewButton(0)
        if not self.initial:
            if prefs.get(u'useDirTree') != self.oldDirTree:
                main.notebook.GetPage(0).set_tree()
            if prefs.get(u'showHiddenDirs') != self.oldSHowHiddenDirs:
                main.notebook.GetPage(0).dirPicker.ShowHidden(prefs.get(u'showHiddenDirs'))

            self.oldDirTree = prefs.get(u'useDirTree')
            self.oldSHowHiddenDirs = prefs.get(u'showHiddenDirs')

            main.show_preview(event)

    def _load_prefs(self, panel, prefs):
        """load preferences from file and apply them to all panels."""
        utils.debug_print(main, 'Loading %s preferences ...'%panel.GetName())
        for child in panel.GetChildren():
            try:
                v = prefs.get(child.GetName(), False)
            except KeyError:
                pass
            else:
                utils.debug_print(main, "   %s = %s"%(child.GetName(), v))
                if isinstance(child, wx.CheckBox) or isinstance(child, wx.RadioButton)\
                  or isinstance(child, wx.SpinCtrl):
                    child.SetValue(v)
                elif isinstance(child, wx.ComboBox) or isinstance(child, wx.TextCtrl):
                    child.SetValue(unicode(v))
                elif isinstance(child, wx.Choice):
                    child.SetSelection(v)


    def _close_diag(self, event):
        self.Close()

    def _on_ok_button(self, event):
        self._on_apply_button(event)
        self.Close()
