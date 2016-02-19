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

"""
This is the main application.
"""

# needed modules:
from __future__ import print_function
import codecs
import gettext
import locale
import os
import platform
import re
import sys
import time

import EnhancedStatusBar as ESB
import about
import app
import classes
import errors
import helpDiag
import langSelect
import preferences
import sorting
import utils
import wx
import wx.lib.dialogs


def create(parent, options):
    return MainWindow(parent, options)

[wxID_MAIN_WINDOW, wxID_MAIN_WINDOWDISPLAY,
wxID_MAIN_WINDOWNOTEBOOK, wxID_MAIN_WINDOWSTATUSBAR1,
wxID_MAIN_WINDOWSTATUSIMAGE,

wxID_MENURENAMER_DESTROY, wxID_MENURENAMER_DESTROYALL,

wxID_MENUHELP_ABOUT, wxID_MENUHELP_HELP,
wxID_MENUHELP_EXAMPLES, wxID_MENUHELP_REHELP,
wxID_MENUHELP_FORMATHELP,

wxID_MENUFILE_EXIT, wxID_MENUFILE_PREVIEW,
wxID_MENUFILE_GO, wxID_MENUFILE_LOADINI,
wxID_MENUFILE_SAVEINI, wxID_MENUFILE_SAVELOG,
wxID_MENUFILE_IMPORT, wxID_MENUFILE_RESET,

wxID_MENUPICKER_ALL, wxID_MENUPICKER_NONE,
wxID_MENUPICKER_WALK, wxID_MENUPICKER_BROWSE,
wxID_MENUPICKER_OK,

wxID_MENUSETTINGS_PREFERENCES, wxID_MENUSETTINGS_LANG,

 ] = [wx.NewId() for __init_menu_edit in range(27)]


class MySplitter(wx.SplitterWindow):
    """Main splitter"""

    def __init__(self, parent):
        wx.SplitterWindow.__init__(self, parent,
                                   style=wx.SP_LIVE_UPDATE | wx.SP_3DSASH | wx.SP_NO_XP_THEME)


class MainWindow(wx.Frame):
    """Main application class"""

    def __init_menubar(self, parent):
        parent.Append(menu=self.menuFile, title=_(u"File"))
        parent.Append(menu=self.menuPicker, title=_(u"Picker"))
        parent.Append(menu=self.menuRenamer, title=_(u"Renamer"))
        parent.Append(menu=self.menuEdit, title=_(u"Settings"))
        parent.Append(menu=self.menuHelp, title=_(u"Help"))
        self.menuPicker.getAllMenu.Enable(False)
        self.menuPicker.getNoneMenu.Enable(False)
        self.menuFile.GoMenu.Enable(False)

    def __init_menu_file(self, parent):
        parent.LoadIniMenu = wx.MenuItem(parent, wxID_MENUFILE_LOADINI,
                                         _(u"&Load Config\tctrl+L"),
                                         self.make_space(_(u"Load configuration from file")))
        parent.LoadIniMenu.SetBitmap(wx.Bitmap(utils.icon_path(u'loadIni.png'),
                                     wx.BITMAP_TYPE_PNG))
        parent.SaveIniMenu = wx.MenuItem(parent, wxID_MENUFILE_SAVEINI,
                                         _(u"&Save Config\tctrl+S"),
                                         self.make_space(_(u"Save configuration to file")))
        parent.SaveIniMenu.SetBitmap(wx.Bitmap(utils.icon_path(u'saveIni.png'),
                                     wx.BITMAP_TYPE_PNG))

        parent.SaveLog = wx.MenuItem(parent, wxID_MENUFILE_SAVELOG,
                                     _(u"&Export to log file"),
                                     self.make_space(_(u"Save current snapshot to a log file")))
        parent.SaveLog.SetBitmap(wx.Bitmap(utils.icon_path(u'CSVto.png'),
                                 wx.BITMAP_TYPE_PNG))

        parent.Import = wx.MenuItem(parent,
                                    wxID_MENUFILE_IMPORT, _(u"&Import from log file"),
                                    self.make_space(_(u"Load a snapshot")))
        parent.Import.SetBitmap(wx.Bitmap(utils.icon_path(u'CSVfrom.png'),
                                wx.BITMAP_TYPE_PNG))

        parent.resetApp = wx.MenuItem(parent, wxID_MENUFILE_RESET,
                                      _(u"&Reset"), self.make_space(_(u"Reset all settings")))
        parent.resetApp.SetBitmap(wx.Bitmap(utils.icon_path(u'preview.png'),
                                  wx.BITMAP_TYPE_PNG))

        parent.PreviewMenu = wx.MenuItem(parent, wxID_MENUFILE_PREVIEW,
                                         _(u"&Preview\tF7"), self.make_space(_(u"Preview selection")))
        parent.PreviewMenu.SetBitmap(wx.Bitmap(utils.icon_path(u'preview.png'),
                                     wx.BITMAP_TYPE_PNG))

        parent.GoMenu = wx.MenuItem(parent, wxID_MENUFILE_GO,
                                    _(u"&Go !\tF8"), self.make_space(_(u"Rename selection")))
        parent.GoMenu.SetBitmap(wx.Bitmap(utils.icon_path(u'go.png'),
                                wx.BITMAP_TYPE_PNG))

        parent.exitMenu = wx.MenuItem(parent, wxID_MENUFILE_EXIT,
                                      _(u"&Quit\tctrl+Q"), self.make_space(_(u"Quit Metamorphose")))
        parent.exitMenu.SetBitmap(wx.Bitmap(utils.icon_path(u'exit.png'),
                                  wx.BITMAP_TYPE_PNG))

        parent.AppendItem(parent.LoadIniMenu)
        parent.AppendItem(parent.SaveIniMenu)
        parent.AppendSeparator()
        parent.AppendItem(parent.SaveLog)
        parent.SaveLog.Enable(False)
        parent.AppendItem(parent.Import)
        parent.AppendSeparator()
        parent.AppendItem(parent.PreviewMenu)
        parent.AppendItem(parent.GoMenu)
        parent.AppendSeparator()
        parent.AppendItem(parent.resetApp)
        parent.AppendItem(parent.exitMenu)

        self.Bind(wx.EVT_MENU, self.save_items_as_text,
                  id=wxID_MENUFILE_SAVELOG)
        self.Bind(wx.EVT_MENU, self.import_items_from_text,
                  id=wxID_MENUFILE_IMPORT)
        self.Bind(wx.EVT_MENU, self.save_config,
                  id=wxID_MENUFILE_SAVEINI)
        self.Bind(wx.EVT_MENU, self.load_config,
                  id=wxID_MENUFILE_LOADINI)
        self.Bind(wx.EVT_MENU, self.on_preview_button,
                  id=wxID_MENUFILE_PREVIEW)
        self.Bind(wx.EVT_MENU, self.rename_items,
                  id=wxID_MENUFILE_GO)
        self.Bind(wx.EVT_MENU, self.on_menu_reset,
                  id=wxID_MENUFILE_RESET)
        self.Bind(wx.EVT_MENU, self.on_menu_exit,
                  id=wxID_MENUFILE_EXIT)

    def __init_menu_renamer(self, parent):
        parent.destroyMenu = wx.MenuItem(parent, wxID_MENURENAMER_DESTROY,
                                         _(u"Delete operation"),
                                         self.make_space(_(u"Delete current operation")))
        parent.destroyMenu.SetBitmap(wx.Bitmap(utils.icon_path(u'errors.ico'),
                                     wx.BITMAP_TYPE_ICO))

        parent.destroyAllMenu = wx.MenuItem(parent, wxID_MENURENAMER_DESTROYALL,
                                            _(u"Delete all operations\tctrl+D"),
                                            self.make_space(_(u"Delete all operations")))
        parent.destroyAllMenu.SetBitmap(wx.Bitmap(utils.icon_path(u'nuke.png'),
                                        wx.BITMAP_TYPE_PNG))

        parent.AppendItem(parent.destroyMenu)
        parent.AppendItem(parent.destroyAllMenu)

        self.Bind(wx.EVT_MENU, self.renamer.view.delete_operation,
                  id=wxID_MENURENAMER_DESTROY)
        self.Bind(wx.EVT_MENU, self.renamer.view.destroy_all_operations,
                  id=wxID_MENURENAMER_DESTROYALL)

    def __init_menu_picker(self, parent):
        parent.browseMenu = wx.MenuItem(parent, wxID_MENUPICKER_BROWSE,
                                        _(u"&Browse...\tF4"),
                                        self.make_space(_(u"Browse for path")))
        parent.browseMenu.SetBitmap(wx.Bitmap(
                                    utils.icon_path(u'browse.png'), wx.BITMAP_TYPE_PNG))
        parent.okMenu = wx.MenuItem(parent, wxID_MENUPICKER_OK,
                                    _(u"&Refresh\tF5"),
                                    self.make_space(_(u"Load or reload current path")))
        parent.okMenu.SetBitmap(wx.Bitmap(utils.icon_path(u'reload.png'),
                                wx.BITMAP_TYPE_PNG))

        parent.getAllMenu = wx.MenuItem(parent, wxID_MENUPICKER_ALL,
                                        _(u"Select &All\tctrl+A"),
                                        self.make_space(_(u"Select all items in picker")))
        parent.getAllMenu.SetBitmap(wx.Bitmap(
                                    utils.icon_path(u'selectAll.png'), wx.BITMAP_TYPE_PNG))
        parent.getNoneMenu = wx.MenuItem(parent, wxID_MENUPICKER_NONE,
                                         _(u"Select &None\tctrl+N"),
                                         self.make_space(_(u"Deselect all items in picker")))
        parent.getNoneMenu.SetBitmap(wx.Bitmap(
                                     utils.icon_path(u'selectNone.png'), wx.BITMAP_TYPE_PNG))
        parent.walkMenu = wx.MenuItem(parent, wxID_MENUPICKER_WALK,
                                      _(u"Recursive &selection\tctrl+R"),
                                      self.make_space(_(u"Get all files in directory and sub-directories, but no folders")))
        parent.walkMenu.SetBitmap(wx.Bitmap(utils.icon_path(u'walk.png'),
                                  wx.BITMAP_TYPE_PNG))

        parent.AppendItem(parent.browseMenu)
        parent.AppendItem(parent.okMenu)
        parent.AppendSeparator()
        parent.AppendItem(parent.getAllMenu)
        parent.AppendItem(parent.getNoneMenu)
        parent.AppendItem(parent.walkMenu)

        self.Bind(wx.EVT_MENU, self.picker.browse_for_path,
                  id=wxID_MENUPICKER_BROWSE)
        self.Bind(wx.EVT_MENU, self.picker.set_path,
                  id=wxID_MENUPICKER_OK)
        self.Bind(wx.EVT_MENU, self.picker.select_none,
                  id=wxID_MENUPICKER_NONE)
        self.Bind(wx.EVT_MENU, self.picker.select_all,
                  id=wxID_MENUPICKER_ALL)
        self.Bind(wx.EVT_MENU, self.picker.walk_from_menu,
                  id=wxID_MENUPICKER_WALK)

    def __init_menu_edit(self, parent):
        parent.PrefsMenu = wx.MenuItem(parent,
                                       wxID_MENUSETTINGS_PREFERENCES, _(u"Preferences"),
                                       self.make_space(_(u"Change your preferences")))

        parent.langMenu = wx.MenuItem(parent,
                                      wxID_MENUSETTINGS_LANG, _(u"Language"),
                                      self.make_space(_(u"Change the language")))

        parent.PrefsMenu.SetBitmap(wx.Bitmap(
                                   utils.icon_path(u'preferences.ico'), wx.BITMAP_TYPE_ICO))
        parent.AppendItem(parent.PrefsMenu)

        parent.langMenu.SetBitmap(wx.Bitmap(
                                  utils.icon_path(u'language.png'), wx.BITMAP_TYPE_PNG))
        parent.AppendItem(parent.langMenu)

        self.Bind(wx.EVT_MENU, self.show_preferences,
                  id=wxID_MENUSETTINGS_PREFERENCES)
        self.Bind(wx.EVT_MENU, self.language_select,
                  id=wxID_MENUSETTINGS_LANG)

    def __init_menu_help(self, parent):
        parent.aboutMenu = wx.MenuItem(parent,
                                       wxID_MENUHELP_ABOUT, _(u"About"),
                                       self.make_space(_(u"Display general information about Metamorphose")))
        parent.aboutMenu.SetBitmap(wx.Bitmap(utils.icon_path(u'about.ico'),
                                   wx.BITMAP_TYPE_ICO))

        parent.helpMenu = wx.MenuItem(parent,
                                      wxID_MENUHELP_HELP, _(u"&Help\tF1"),
                                      self.make_space(_(u"How to use Metamorphose")))
        parent.helpMenu.SetBitmap(wx.Bitmap(utils.icon_path(u'help.ico'),
                                  wx.BITMAP_TYPE_ICO))

        parent.examplesMenu = wx.MenuItem(parent,
                                          wxID_MENUHELP_EXAMPLES, _(u"&Examples\tF2"),
                                          self.make_space(_(u"Some useful examples")))
        parent.examplesMenu.SetBitmap(wx.Bitmap(
                                      utils.icon_path(u'examples.ico'), wx.BITMAP_TYPE_ICO))

        parent.FormatHelpMenu = wx.MenuItem(parent,
                                            wxID_MENUHELP_FORMATHELP, _(u"&Date && Time Formats"),
                                            self.make_space(_(u"Display a reference for Date & Time formats")))
        parent.FormatHelpMenu.SetBitmap(wx.Bitmap(
                                        utils.icon_path(u'date_time.ico'), wx.BITMAP_TYPE_ICO))

        parent.REhelpMenu = wx.MenuItem(parent,
                                        wxID_MENUHELP_REHELP, _(u"&Regular Expressions"),
                                        self.make_space(_(u"Display a regular expression reference")))
        parent.REhelpMenu.SetBitmap(wx.Bitmap(utils.icon_path(u're.ico'),
                                    wx.BITMAP_TYPE_ICO))

        parent.AppendItem(parent.aboutMenu)
        parent.AppendItem(parent.helpMenu)
        parent.AppendItem(parent.examplesMenu)
        parent.AppendItem(parent.FormatHelpMenu)
        parent.AppendItem(parent.REhelpMenu)

        self.Bind(wx.EVT_MENU, self.show_about,
                  id=wxID_MENUHELP_ABOUT)
        self.Bind(wx.EVT_MENU, self.show_help,
                  id=wxID_MENUHELP_HELP)
        self.Bind(wx.EVT_MENU, self.show_small_help,
                  id=wxID_MENUHELP_EXAMPLES)
        self.Bind(wx.EVT_MENU, self.show_small_help,
                  id=wxID_MENUHELP_FORMATHELP)
        self.Bind(wx.EVT_MENU, self.show_small_help,
                  id=wxID_MENUHELP_REHELP)

    def __init_notebook(self):
        parent = self.notebook

        # init Core classes
        self.picker = picker.Core(parent, self)
        self.sorting = sorting.Core(parent, self)
        self.errors = errors.Core(parent, self)
        self.renamer = renamer.Core(parent, self)

        # list containing notebook images
        il = wx.ImageList(16, 16)
        img0 = il.Add(wx.Bitmap(utils.icon_path(u'picker.ico'),
                      wx.BITMAP_TYPE_ICO))
        img1 = il.Add(wx.Bitmap(utils.icon_path(u'main.ico'),
                      wx.BITMAP_TYPE_ICO))
        img2 = il.Add(wx.Bitmap(utils.icon_path(u'sorting.ico'),
                      wx.BITMAP_TYPE_ICO))
        img3 = il.Add(wx.Bitmap(utils.icon_path(u'errors.ico'),
                      wx.BITMAP_TYPE_ICO))
        parent.AssignImageList(il)

        # add notebook pages to notebook
        parent.AddPage(self.picker.view, _(u"Picker"), True, img0)
        parent.AddPage(self.renamer.view, _(u"- Renamer -"), False, img1)
        parent.AddPage(self.sorting.view, _(u"Sorting"), False, img2)
        parent.AddPage(self.errors.view, _(u"Errors/Warnings: %s") % 0, False, img3)

    def __init_sizer(self):
        mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.splitter, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(mainSizer)

    def __init_utils(self):
        self.menuFile = wx.Menu()
        self.menuPicker = wx.Menu()
        self.menuEdit = wx.Menu()
        self.menuHelp = wx.Menu()
        self.menuBar = wx.MenuBar()
        self.menuRenamer = wx.Menu()
        self.__init_menu_file(self.menuFile)
        self.__init_menu_picker(self.menuPicker)
        self.__init_menu_renamer(self.menuRenamer)
        self.__init_menu_edit(self.menuEdit)
        self.__init_menu_help(self.menuHelp)
        self.__init_menubar(self.menuBar)
        self.SetMenuBar(self.menuBar)

    def __init_fonts(self):
        """Get fonts from system or specify own."""
        if wx.Platform == '__WXGTK__':
            sysFont = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
            app.fontParams = {
                'size': sysFont.GetPixelSize()[0],
                'style': sysFont.GetStyle(),
                'family': sysFont.GetFamily(),
                'weight': sysFont.GetWeight(),
            }
        else:
            app.fontParams = {
                'size': 9,
                'style': wx.NORMAL,
                'family': wx.DEFAULT,
                'weight': wx.NORMAL,
            }
        #print(app.fontParams)
        self.SetFont(wx.Font(
                     app.fontParams['size'],
                     app.fontParams['family'],
                     app.fontParams['style'],
                     app.fontParams['weight'])
                     )

    def __init_ctrls(self, prnt):
        wx.SystemOptions.SetOption('msw.notebook.themed-background', '0')
        if app.debug:
            self.SetTitle(u"Métamorphose 2 v. %s -- DEBUG MODE" % app.version)
        else:
            self.SetTitle(u"Métamorphose 2 (beta)")
        self.SetBackgroundColour(wx.NullColour)
        self.SetAutoLayout(False)
        self.SetStatusBarPane(0)
        self.SetIcon(wx.Icon(utils.icon_path(u'metamorphose.ico'), wx.BITMAP_TYPE_ICO))
        self.SetThemeEnabled(True)
        self.__init_fonts()

        self.statusBar1 = ESB.EnhancedStatusBar(id=wxID_MAIN_WINDOWSTATUSBAR1,
                                                name=u'statusBar1', parent=self)
        self.SetStatusBar(self.statusBar1)


        self.statusImage = wx.StaticBitmap(bitmap=self.statusImages[u'eyes'],
                                           id=wxID_MAIN_WINDOWSTATUSIMAGE, name=u'statusImage',
                                           parent=self.statusBar1, size=wx.Size(-1, 16), style=0)
        self.statusBar1.AddWidget(self.statusImage, ESB.ESB_ALIGN_LEFT)

        self.splitter = MySplitter(self)

        # notebook
        self.notebook = wx.Notebook(id=wxID_MAIN_WINDOWNOTEBOOK,
                                    name=u'notebook', parent=self.splitter,
                                    style=wx.NB_TOP | wx.NO_BORDER)
        self.notebook.SetThemeEnabled(True)

        self.bottomWindow = bottomWindow.MainPanel(self.splitter, self)
        self.SetMinSize(wx.Size(-1, 600))

        self.splitter.SetMinimumPaneSize(40)

        if wx.Platform == '__WXGTK__':
            split = -210
        elif wx.Platform == '__WXMSW__':
            split = -200
        else:
            split = -205
        self.splitter.SplitHorizontally(self.notebook, self.bottomWindow, split)

    def set_language(self):
        """
        Determine language to be loaded depending on : setting file, CLI option,
        or neither.
        Apply language to interface.
        """
        app.debug_print("== Interface Localization ==")

        # reference:
        locales = {
            #u'ar' : (wx.LANGUAGE_ARABIC, u'ar_SA.UTF-8'),
            #u'de' : (wx.LANGUAGE_GERMAN, u'de_DE.UTF-8'),
            #u'el' : (wx.LANGUAGE_GREEK, u'el_GR.UTF-8'),
            #u'en_GB' : (wx.LANGUAGE_ENGLISH_UK, u'en_GB.UTF-8'),
            u'en_US': (wx.LANGUAGE_ENGLISH_US, u'en_US.UTF-8'),
            u'es': (wx.LANGUAGE_SPANISH, u'es_ES.UTF-8'),
            u'fr': (wx.LANGUAGE_FRENCH, u'fr_FR.UTF-8'),
            #u'he' : (wx.LANGUAGE_HEBREW, u'he_IL.UTF-8'),
            #u'hu' : (wx.LANGUAGE_HUNGARIAN, u'hu_HU.UTF-8'),
            #u'it' : (wx.LANGUAGE_ITALIAN, u'it_IT.UTF-8'),
            #u'ja' : (wx.LANGUAGE_JAPANESE, u'ja_JP.UTF-8'),
            #u'pl' : (wx.LANGUAGE_POLISH, u'pl_PL.UTF-8'),
            #u'pt_BR' : (wx.LANGUAGE_PORTUGUESE_BRAZILIAN, u'pt_BR.UTF-8'),
            #u'ru' : (wx.LANGUAGE_RUSSIAN, u'ru_RU.UTF-8'),
            #u'sv' : (wx.LANGUAGE_SWEDISH, u'sv_SE.UTF-8'),
            #u'tr' : (wx.LANGUAGE_TURKISH, u'tr_TR.UTF-8'),
            #u'zh_CN' : (wx.LANGUAGE_CHINESE_SIMPLIFIED, u'zh_CN.UTF-8'),
        }

        # right-to-left languages:
        rightToLeftLanguages = ('ar', 'dv', 'fa', 'ha', 'he', 'ps', 'ur', 'yi')
        '''
        syslang = locale.getdefaultlocale()[0]
        if syslang in locales:
            language = syslang
        '''
        # get language from file if not specified from command line
        if not app.language:
            try:  # see if language file exist
                langIni = codecs.open(utils.get_user_path(u'language.ini'), 'r', 'utf-8')
            except IOError:  # have user choose language
                language = self.language_select(0)
            else:  # get language from file
                language = langIni.read().strip()
        else:
            language = app.language

        try:
            locales[language]
        except KeyError:
            msg = u"Could not initialize language: '%s'.\nContinuing in " % language
            msg += u"American English (en_US)\n"
            print(msg)
            language = 'en_US'

        # needed for calendar and other things, send all logs to stderr
        wx.Log.SetActiveTarget(wx.LogStderr())

        # set locale and language
        wx.Locale(locales[language][0], wx.LOCALE_LOAD_DEFAULT)

        try:
            Lang = gettext.translation(u'metamorphose2', app.locale_path(language),
                                       languages=[locales[language][1]])
        except IOError:
            print("Could not find the translation file for '%s'." % language)
            print("Try running messages/update_langs.sh\n")
            sys.exit(1)

        Lang.install(unicode=True)

        # set some globals
        if language not in rightToLeftLanguages:
            self.langLTR = True
            self.alignment = wx.ALIGN_LEFT
        else:
            self.langLTR = False
            self.alignment = wx.ALIGN_RIGHT
        app.language = language
        app.debug_print("Set language: " + app.language)

        self.encoding = unicode(locale.getlocale()[1])
        app.debug_print("Set encoding: " + self.encoding)

        # to get some language settings to display properly:
        if platform.system() in ('Linux', 'FreeBSD'):
            try:
                os.environ['LANG'] = locales[language][1]
            except (ValueError, KeyError):
                pass
        app.debug_print("============================")
        app.debug_print("")


    def __init__(self, prnt, options):
        # Important variables needed throughout the application classes
        self.warn = [] # warnings
        self.bad = [] # errors
        self.errorLog = [] # all errors go here
        self.items = [] # items to rename
        self.spacer = u" " * 6 # spacer for status messages (to clear image)
        # icons used for status bar messages
        self.statusImages = {
            u'failed': wx.Bitmap(utils.icon_path(u'failed_sb.ico'),
                                 wx.BITMAP_TYPE_ICO),
            u'wait': wx.Bitmap(utils.icon_path(u'wait.png'),
                               wx.BITMAP_TYPE_PNG),
            u'warn': wx.Bitmap(utils.icon_path(u'warn_sb.ico'),
                               wx.BITMAP_TYPE_ICO),
            u'complete': wx.Bitmap(utils.icon_path(u'complete.ico'),
                                   wx.BITMAP_TYPE_ICO),
            u'eyes': wx.Bitmap(utils.icon_path(u'eyes.png'),
                               wx.BITMAP_TYPE_PNG),
        }

        app.debug_print("Init MainWindow")
        wx.Frame.__init__(self, id=wxID_MAIN_WINDOW, name=u'MainWindow',
                          parent=prnt, style=wx.DEFAULT_FRAME_STYLE)
        app.debug_print("")

        app.debug_print("======== System Info =======")
        app.debug_print("Operating System: %s - %s - %s" % (platform.system(), platform.release(), platform.version()))
        app.debug_print("Python version: %s" % platform.python_version())
        app.debug_print("wxPython version: %s" % wx.version())
        app.debug_print("============================")
        app.debug_print("")

        # first run?
        utils.init_environment()

        self.set_language()

        # import these modules here since they need language settings activated
        global renamer
        import renamer
        global configs
        import configs
        global picker
        import picker
        global bottomWindow
        import bottomWindow

        # initialize preferences
        app.debug_print("======== Preferences =======")
        app.prefs = preferences.Methods()
        app.debug_print("============================")
        app.debug_print("")

        # build main GUI
        self.__init_ctrls(prnt)

        # clear undo if set in preferences:
        if app.prefs.get(u'clearUndo'):
            try:
                originalFile = codecs.open(utils.get_user_path(u'undo/original.bak'),
                                           'w', "utf-8")
                originalFile.write('')
                renamedFile = codecs.open(utils.get_user_path(u'undo/renamed.bak'),
                                          'w', "utf-8")
                renamedFile.write('')
            except IOError, error:
                utils.make_err_msg(_(u"%s\n\nCould not clear undo") % error,
                                   _(u"Error"))
                pass

        # construct rest of GUI:
        self.__init_notebook()
        self.__init_utils()
        self.__init_sizer()
        # call this after sizer to place properly:
        self.Center(wx.HORIZONTAL | wx.VERTICAL)

        # Load config from command line
        if options['configFilePath']:
            app.debug_print("Load config from CLI")
            configs.LoadConfig(self, options['configFilePath'])

        # Set root directory from command line arguments:
        if options['path']:
            path = options['path'].rstrip()
            self.picker.view.path.SetValue(path)
            self.picker.set_path(True)

#
#--- MISC STUFF: ------------------------------------------------------------#
#
    # Little functions to make repetitive stuff easier to implement.

    def make_space(self, statusText):
        """add spacing for translation"""
        #if self.langLTR:
        #    return self.spacer+statusText
        #else:
        return self.spacer + statusText

    def show_preview(self, event):
        """
        This function is called by basically every widget in the app.
        It calls the preview function, if the user has set so in preferences.
        """
        if event and self.bottomWindow.autoPreview.GetValue():
            self.on_preview_button(False)

    def language_select(self, event):
        """Open language selection dialog."""
        # if triggered from event, language has already been loaded,
        # and we will be changing it. No event = no language file
        if event == 0:
            Title = u'\m/ (>_<) \m/'
        else:
            Title = _(u"Language")
            event = app.language
        # show the language choices
        dlg = langSelect.create(self, Title, event)
        if dlg.ShowModal() == wx.ID_OK:
            language = dlg.GetLanguage()
            dlg.Destroy()
            if app.language != language:
                self.change_language(language, event)
            return language

    def change_language(self, language, event):
        """Write given language to 'language.ini' file."""
        try:
            langFile = codecs.open(utils.get_user_path(u'language.ini'), 'w', 'utf-8')
        except IOError, error:
            utils.make_err_msg(unicode(error), u"Error")
            pass
        else:
            langFile.write(language)
            langFile.close()
        if event:
            msg = _(u"\n\nYou will need to restart Metamorphose to change the language.")
            msg += _(u"\n\nClose out of Metamorphose now?")
            msg = language + msg
            title = _(u"Change the Language")
            # Restart app automatically if not in windows
            if utils.make_yesno_dlg(msg, title):
                if platform.system() != 'Windows':
                    if wx.Process.Open(app.get_real_path(sys.argv[0])):
                        self.Close()
                else:
                    self.Close()

    def set_status_msg(self, msg, img):
        """Set status bar text and image."""
        self.statusImage.SetBitmap(self.statusImages[img])
        self.SetStatusText(self.make_space(msg))
        app.debug_print(u"status message: '%s'" % msg)

#
#--- MENU ACTIONS: -----------------------------------------------------------#
#

    def on_menu_exit(self, event):
        self.Close()

    def on_menu_reset(self, event):
        yes = utils.make_yesno_dlg(_(u'Are you sure you want to reset?'), _(u'Are you sure?'))
        if yes:
            configs.load(self, app.get_real_path('default.cfg'))
            self.picker.view.path.SetValue(u'')
            self.picker.clear_all()

    def save_config(self, event):
        configs.save(self)

    def load_config(self, event):
        configs.load(self)

    def save_items_as_text(self, event):
        """Export current selection as CSV file."""
        if hasattr(self, 'toRename'):
            CSVfile = ""
            q = app.prefs.get('logEnclose')
            sep = app.prefs.get('logSeparator')
            ext = app.prefs.get('logFextension')

            if app.showTimes:
                t = time.time()

            # create file contents
            for original, renamed in self.toRename:
                CSVfile += unicode(q + original[0] + q + sep + q + renamed[0] + q + '\n')

            if app.showTimes:
                print("Export file contents for %s items: %s" % (len(self.toRename), (time.time() - t)))

            # triggered by menu, allow to choose output file
            if event:
                dlg = wx.FileDialog(self, message=_(u"Save current items as ..."),
                                    defaultDir='', defaultFile=u'.%s' % ext,
                                    wildcard=_(u"CSV file (*.%s)") % ext + u'|*.%s' % ext,
                                    style=wx.SAVE | wx.OVERWRITE_PROMPT
                                    )
                if dlg.ShowModal() == wx.ID_OK:
                    # attempt to write file
                    utils.write_file(dlg.GetPath(), CSVfile)
                dlg.Destroy()
            # auto logging, generate file name
            else:
                file = time.strftime("undo_%Y-%m-%d_%Hh%Mm%Ss",
                                     time.localtime()) + '.' + app.prefs.get('logFextension')
                path = os.path.join(app.prefs.get(u'logLocation'), file)
                utils.write_file(path, CSVfile)

    def import_items_from_text(self, event):
        """Import item selection from text file."""
        if app.prefs.get('logLocation') != '':
            path = app.prefs.get('logLocation')
        else:
            path = utils.get_user_path(u'undo')

        # settings from preferences
        ext = app.prefs.get('logFextension')
        q = app.prefs.get('logEnclose')
        sep = app.prefs.get('logSeparator')

        wildOnes = _(u"Log file") + u" (*.%s)|*.%s|" % (ext, ext) + \
            _(u"All files") + "(*.*)|*.*"

        # file open dialog
        dlg = wx.FileDialog(
                            self, message=_(u"Import selection from ..."), defaultDir=path,
                            defaultFile=u'', wildcard=wildOnes,
                            style=wx.OPEN | wx.CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            original = []
            renamed = []
            unloadbles = ""
            f = dlg.GetPath()

            # undo files have order reversed
            if os.path.basename(f)[0:5] == 'undo_':
                o = 1
                r = 0
            else:
                o = 0
                r = 1
            f = codecs.open(f, 'r', 'utf_8')
            i = 0
            for line in f.readlines():
                i += 1
                line = line.lstrip(q).rstrip(q + '\n').split(q + sep + q)
                # check for existance of every item
                if os.path.exists(line[o]):
                    original.append((line[o], 1))
                    renamed.append([line[r], False])
                else:
                    unloadbles += "%s\n" % line[o]

            # set up for display
            self.toRename = zip(original, renamed)
            self.picker.view.path.SetValue('')
            self.picker.clear_all()

            # only allow rename if there are items
            if len(self.toRename) != i:
                msg = _(u"These items could not be loaded, it doesn't look like they exist :\n\n")
                msg += unloadbles
                dlg = wx.lib.dialogs.ScrolledMessageDialog(self, msg,
                                                           "Could not load all items")
                dlg.ShowModal()
            if len(self.toRename) != 0:
                self.bottomWindow.go.Enable(True)
                self.menuFile.GoMenu.Enable(True)
                self.currentItem = None
                self.display_results(True)
            f.close()

    def show_help(self, event):
        """Opens main help dialog."""
        helpDiag.create(self).Show()

    def show_small_help(self, event):
        """Opens generic html help dialog."""
        if event.GetId() == wxID_MENUHELP_REHELP:
            helpFile = u'REhelp.html'
            Title = _(u"Regular Expression Help")
            Icon = u're'
        elif event.GetId() == wxID_MENUHELP_FORMATHELP:
            helpFile = u'format.html'
            Title = _(u"Date and Time Formatting Help")
            Icon = u'date_time'
        elif event.GetId() == wxID_MENUHELP_EXAMPLES:
            helpFile = u'examples.html'
            Title = _(u"Examples")
            Icon = u'examples'
        return classes.SmallHelp(self, helpFile, Title, Icon).Show()

    def show_about(self, event):
        """Opens about dialog."""
        aboutDlg = about.create(self)
        aboutDlg.CentreOnParent()
        aboutDlg.ShowModal()
        aboutDlg.Destroy()

    def show_preferences(self, event):
        """Opens preferences dialog."""
        prefDiag = preferences.create_dialog(self)
        prefDiag.ShowModal()
        prefDiag.Destroy()
        # to re-init color definitions
        self.bottomWindow.set_preferences()

#
#--- DISPLAY RESULTS ---------------------------------------------------------#
#

    def display_results(self, showDirs=False):
        """
        Resets the bottom preview virtual list, then sets amount of items and the
        correct imagelist to use.
        """
        self.errors.clear()

        pickerList = self.picker.view.ItemList
        display = self.bottomWindow.display
        #display.Enable(False)
        usedOperations = self.renamer.view.usedOperations
        # show complete path in new name
        if not showDirs:
            for i in range(usedOperations.GetItemCount()):
                op = usedOperations.GetItemText(i)
                if re.search(_("directory"), op):
                    showDirs = True
                    break
        display.showDirs = showDirs
        display.mode = 'preview'

        # set the image list
        if app.prefs.get('showPreviewIcons'):
            display.imgs = pickerList.imgs
        else:
            display.imgs = wx.ImageList(16, 16)
            display.folderIco = display.imgs.Add(wx.Bitmap(
                                                 utils.icon_path(u'folder16.png'), wx.BITMAP_TYPE_PNG))
            display.fileIco = display.imgs.Add(wx.Bitmap(
                                               utils.icon_path(u'file16.png'), wx.BITMAP_TYPE_PNG))
        display.SetImageList(display.imgs, wx.IMAGE_LIST_SMALL)

        display.DeleteAllItems()
        display.SetItemCount(len(self.toRename))

        #display.Enable(True)

        # auto resize column:
        #display.SetColumnWidth(2,-1)
        if display.GetColumnWidth(2) < 135:
            display.SetColumnWidth(2, 135)

        # show the last warning/error
        if self.warn:
            display.EnsureVisible(self.warn[-1])
        elif self.bad:
            display.EnsureVisible(self.bad[-1])

        # show the currently selected item
        try:
            display.Select(self.currentItem, True)
        except TypeError:  # may need AttributeError
            pass
        else:
            display.EnsureVisible(self.currentItem)

#
#--- CHANGE ITEM POSITION IN LIST --------------------------------------------#
#

    def on_item_selected(self, event):
        """Set the selected item."""
        self.currentItem = event.m_itemIndex

    def change_item_order(self, change):
        """Move the selected item."""
        if self.currentItem:
            try:
                moveTo = self.currentItem + change
            except TypeError:
                if change == u'top':
                    moveTo = 0
                else:
                    moveTo = len(self.items)-1
                pass

            if moveTo > len(self.items):
                moveTo = len(self.items)-1
            if moveTo < 0:
                moveTo = 0

            old = self.items[self.currentItem]
            del self.items[self.currentItem]
            self.items.insert(moveTo, old)
            self.currentItem = moveTo
            self.on_preview_button(0)

#
#--- NAME GENERATION ---------------------------------------------------------#
#

    def on_preview_button(self, event):
        utils.set_busy(True)
        self.renamer.preview(event)
        utils.set_busy(False)

#
#--- RENAMING: ---------------------------------------------------------------#
#

    def rename_items(self, event):
        """Rename selected items."""
        self.renamer.rename(event)

    def undo_rename(self, event):
        """Undo the last renaming operation."""
        self.renamer.undo(event)
