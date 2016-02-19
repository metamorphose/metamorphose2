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
import codecs
import logging
import os

import app
import automation
import colors
from dialog import Dialog
import display
import errorCheck
import general
import utils
import sys
import wx
import platform


def create_dialog(parent, initial=False):
    """
    Create and return the preferences dialog.
    """
    return Dialog(parent, Methods(), initial)


class Methods:
    """
    Preference methods.
    """
    def __init__(self,):
        self.header = u'Version=%s\n' % app.version
        self.prefs = False
        self.key_error = False
        self.prefFilePath = self.__find_pref_file()
        self.__load_preferences()

    def __find_pref_file(self):
        prefFile = utils.get_user_path(u'preferences.ini')
        return prefFile

    def __open_pref_file(self, path, mode):
        app.debug_print("Opening as '%s': %s" % (mode, path))
        prefFile = codecs.open(path, mode, 'utf-8')
        return prefFile

    def __use_defaults(self):
        """
        Use the default preferences file.
        """
        app.debug_print("Using default preferences")
        # show preferences
        prefDiag = Dialog(None, self, initial=True)
        prefDiag.ShowModal()
        try:
            prefDiag.Destroy()
        except wx._core.PyDeadObjectError:
            app.debug_print("=======================")
            pass

    def __read_file(self, path):
        """
        Process file and return preferences dictionary.
        """
        prefFile = self.__open_pref_file(path, 'r')

        prefFile.seek(0)
        version = prefFile.readline().strip()[8:]

        # TODO preferences from a prior version
        if version != app.prefsVersion:
            app.debug_print("Old version found")

        prefFile.seek(0)
        prefs = {}
        for line in prefFile:
            if line.find('=') > 0:
                line = line.replace(u'\n', '')
                split = line.split('=')
                try:
                    prefs[split[0]] = int(split[1])
                except KeyError:
                    pass
                except ValueError:
                    prefs[split[0]] = unicode(split[1])
                    pass
        prefFile.close()
        return prefs

    def __load_preferences(self):
        """
        Get values from file (one way or another)
        """
        prefFile = self.__find_pref_file()
        app.debug_print("Try to load preferences from file")
        # make sure the file exist and is filled:
        if not os.path.exists(prefFile) or os.path.getsize(prefFile) < 5:
            app.debug_print("File does not exist or is empty: Using default preferences")
            prefFile = app.get_real_path(os.path.join('preferences', 'default.ini'))
        self.prefFilePath = prefFile
        prefs = self.__read_file(prefFile)

        # windows-compatible?
        if platform.system() != 'Windows':
            win_compatible = False
        if prefs.get(u'useWinChars', win_compatible):
            prefs[u'bad_chars'] = (u'\\', u'/', u':', u'*', u'?', u'"', u'>', u'<', u'|')
        if prefs.get(u'useWinNames', win_compatible):
            prefs[u'bad_win_words'] = (u'con', u'prn', u'aux', u'clock$',
                                       u'nul', u'com1', u'com2', u'com3', u'com4', u'com5', u'com6', u'com7',
                                       u'com8', u'com9', u'lpt1', u'lpt2', u'lpt3', u'lpt4', u'lpt5', u'lpt6',
                                       u'lpt7', u'lpt8', u'lpt9')

        prefs[u'backgroundColor'] = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        prefs[u'highlightColor'] = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        prefs[u'highlightTextColor'] = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        prefs[u'textColor'] = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
        app.debug_print("Loaded %s preferences" % len(prefs))
        self.prefs = prefs

    def set_prefs(self, prefDialog):
        """
        Get values from panels and set to file.
        """
        self.prefFilePath = self.__find_pref_file()
        prefFile = self.__open_pref_file(self.prefFilePath, 'w')
        options = self.header

        app.debug_print("Preferences to save:")
        # get all pages in notebook
        for i in range(prefDialog.notebook.GetPageCount()):
            # section header is page name
            options += u'\n[%s]\n' % prefDialog.notebook.GetPageText(i)

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
                elif isinstance(child, wx.DirPickerCtrl):
                    value = child.GetPath()
                    type = 'DirPickerCtrl'
                elif isinstance(child, wx.FilePickerCtrl):
                    value = child.GetPath()
                    type = 'FilePickerCtrl'
                elif isinstance(child, wx.ColourPickerCtrl):
                    value = child.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
                    type = 'ColourPickerCtrl'

                if value is not None:
                    name = child.GetName()
                    options += u'%s=%s\n' % (name, value)
                    app.debug_print("    %s (%s) = %s" % (name, type, value))
        prefFile.write(options)
        prefFile.close()
        self.__load_preferences()

    def get(self, preference):
        """
        Attempt to load a preference setting
        Load or recreate preference file if needed.
        """
        try:
            return self.prefs[preference]
        except KeyError:
            if not self.key_error:
                msg = _(u"\nThe preferences file is outdated or corrupt.")
                msg += u"\n%s" % self.prefFilePath
                utils.make_err_msg(msg, _(u"Problem with preferences"))
            # set this here so we don't see the message for evey missing key
            self.key_error = True
            raise KeyError

    def get_all(self):
        """
        Get all preferences.
        Will attempt to load from file if no preferences are defined.
        """
        if not self.prefs:
            self.__load_preferences()
        return self.prefs
