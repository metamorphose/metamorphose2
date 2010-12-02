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

"""
Selects and deselects items based on user input.
Supports direct selection, regular expression filters, and attribute filters.
"""

from __future__ import print_function
import utils
import classes
import sys
import os
import re
import sre_constants
import time

import wxPickerView
# TODO need to make core independant of wxWidgets
import wx


### Handle loading parameters
class Parameters(classes.Parameters):
    def __init__(self, Panel):
        # set the picker panel
        self.Panel = Panel
        # define the operation type used to retrieve values
        self.set_value_method()

    # load all needed panel values to instance
    def load(self):
        root = self.getValue(self.Panel.path)
        self.setRootPath(root)
        widgets = (
            'foldersOn', # grab folders
            'filesOn', # grab files
            'notType', # invert filter
            'FilterSel',
            'filterByRE',
            'ignoreCase',
            'useLocale',
            'walkIt', # recursive
            'walkDepth',
        )
        return self.set_parameters(widgets)

    # determine if root path is usable
    def setRootPath(self, root):
        utils.debug_print(main, "Examining : %s"%root)
        
        self.root = False
        # don't do anything for blank path
        if not root:
            main.set_status_msg('',u'eyes')
        # don't do anything unless path is readable
        elif not os.access(root, os.R_OK):
            main.set_status_msg(_(u"Cannot read path!"),u'warn')
            #main.bottomWindow.display.DeleteAllItems()
        # all good
        else:
            self.root = root



class Core():
    def __init__(self, parent, MainWindow):

        self.CommonSearches = (
                 ("" , ""),
                 ( _(u"- audio") , u"\.(mp3|wav|ogg|flac|wma|aiff|aac|m3u|mid|ra|ram)$" ),
                 ( _(u"- image") , u"\.(bmp|jpg|jpeg|png|svg|ico|tif|tiff|gif|psd|ai|thm|nef)$" ),
                 ( _(u"- video") , u"\.(avi|mpg|mpeg|mpe|mp4|m4e|wmv|divx|flc|mov|ogm)$" ),
                 ( _(u"- office related") , u"\.(txt|csv|rtf|doc|otf|xls|pps|ppt)$" ),
                 ( _(u"- web related") , u"\.(htm|html|php|css|js|asp|cgi|swf)$" ),
                 ( _(u"- programming") , u"\.(py|pyc|php|pl|h|c|cpp|cxx|jar|java|js|tcl)$" ),
                 ( _(u"- compressed") , u"\.(zip|tar|7z|ace|gz|tgz|rar|r\d{1,3}|cab|bz2)$" ),
                 ( _(u"- an extension") , u"^.+\..+$" ),
                 ( _(u"- only an extension") , u"^\." ),
            )
        self.CustomSearches = {}

        global main
        main = MainWindow

        self.Panel = wxPickerView.Panel(self, parent, MainWindow)
        self.params = Parameters(self.Panel)
        self.joinedItems = []


    # wrappers to acces Panel

    def set_status_msg(self, msg, ico):
        main.set_status_msg(msg, ico)

    def addItemsToPanel(self, folders, files):
        self.Panel.ItemList.add_items(self.params.root, folders, files)

    def getItemsInPanelCount(self):
        return self.Panel.ItemList.GetItemCount()

    def selectAllItemsInPanel(self, event=True):
        self.Panel.select_all(event)

    def selectNoItemsInPanel(self, event=True):
        self.Panel.select_none(event)

    def browseForPath(self, event=True):
        self.Panel.browse_for_path(event)

    def walk_from_menu(self, event):
        self.Panel.walk_from_menu()
        self.refresh(True)

    def enablePanelWidget(self, widget, state):
        getattr(self.Panel, widget).Enable(state)

    def deleteAllItemsInPanel(self):
        self.Panel.ItemList.DeleteAllItems()

    def setPanelPath(self, event):
        self.Panel.set_path(event)
        self.refresh(True)

    def enable_buttons(self):
        self.Panel.enable_buttons()


    # helpers

    def clearJoinedItems(self):
        self.joinedItems = []

    def returnSorted(self):
        return main.sorting.sortItems(self.joinedItems)

    def clearALL(self):
        self.clearJoinedItems()
        self.deleteAllItemsInPanel()

    def refreshDirTree(self):
        if main.prefs.get(u'useDirTree'):
            dirPicker = self.Panel.dirPicker
            itemId = self.Panel.dirPicker.GetTreeCtrl().GetSelection()
            dirPicker.GetTreeCtrl().CollapseAndReset(itemId)
            dirPicker.GetTreeCtrl().Expand(itemId)


    def remove_items_by_name(self, itemNames):
    	for name in itemNames:
            displayedName = name.replace(self.params.root, '')

            if os.path.split(displayedName)[0] == os.sep:
                displayedName = displayedName[1:]

            ID = self.Panel.ItemList.FindItem(0,displayedName)
            item = wx.ListItem()
            item.SetId(ID)
            item.SetBackgroundColour(utils.BackgroundClr)
            item.SetTextColour(utils.TxtClr)
            self.Panel.ItemList.SetItem(item)

            # remove from item list
            IsFile = os.path.isfile(name)
            fullItem = [name, IsFile]
            self.joinedItems.remove(fullItem)
            
            self.enable_buttons()


    def setInitial(self):
        self.clearALL()
        main.recursiveFolderOn = False
        utils.set_busy(True)
        self.enablePanelWidget('selectNone', False)
        main.menuPicker.getNoneMenu.Enable(False)
        main.bottomWindow.go.Enable(False)


    # get the filter used when loading items from selected directory
    def getFilter(self, params):
            filterSel = params.FilterSel

            # are we using a built in filter ?
            if filterSel != '' and self.Panel.get_in_searches(filterSel):
                filter = self.Panel.get_in_searches(filterSel)
            else:
                filter = filterSel

            # are we searching by regular expression ?
            if filter and params.filterByRE:
                ignoreCase = params.ignoreCase
                useLocale = params.useLocale
                try:
                    # compile according to options:
                    if ignoreCase and useLocale:
                        filter = re.compile(filter, re.IGNORECASE | re.UNICODE)
                    elif ignoreCase:
                        filter = re.compile(filter, re.IGNORECASE)
                    elif useLocale:
                        filter = re.compile(filter, re.UNICODE)
                    else:
                        filter = re.compile(filter)
                except sre_constants.error as err:
                    main.set_status_msg(_(u"Regular-Expression: %s")%err,u'warn')
                    main.REmsg = True
                    filter = re.compile(r'')
                    pass
                useRE = True
            else:
                filter = filter.lower()
                useRE = False

            return filter, useRE

    # core logic

    """
    Grab items from a specified directory, either as a listing or as a
    walk, and filter out entries based on user settings.
    Files and folders are seperated for proper sorting.
    Called, depending on user preferences,
    from almost every widget in the picker panel, and from
    the main application class.
    """
    def refresh(self, event):
        files = [] #files will go here
        folders = [] #folders will go here
        error = False
        
        params = self.params.load()

        if params.root is False:
            self.deleteAllItemsInPanel()
        # OK, load items up:
        else:
            self.setInitial()

            main.set_status_msg(_(u"Getting directory contents please wait ..."),u'wait')

            if main.show_times:
                t = time.time()

            filter, useRE = self.getFilter(params)

            # create the search (filtering) operations ...
            notType = params.notType

            # normal filtering:
            if filter and not useRE:
                def filterFolders(entry):
                    if filter in entry.lower() and not notType:
                        folders.append(entry)
                    if filter not in entry.lower() and notType:
                        folders.append(entry)
                def filterFiles(entry):
                    if filter in entry.lower() and not notType:
                        files.append(entry)
                    if filter not in entry.lower() and notType:
                        files.append(entry)
            # regular expression filtering
            elif filter and useRE:
                def filterFolders(entry):
                    if filter.search(entry) and not notType:
                        folders.append(entry)
                    if not filter.search(entry) and notType:
                        folders.append(entry)
                def filterFiles(entry):
                    if filter.search(entry) and not notType:
                        files.append(entry)
                    if not filter.search(entry) and notType:
                        files.append(entry)
            # no filtering:
            else:
                def filterFolders(entry):
                    folders.append(entry)
                def filterFiles(entry):
                    files.append(entry)

            # define here for speed boost
            def isDir(entry):
                    join = os.path.join(params.root, entry)
                    return os.path.isdir(join)

            def getEncodedName(filename):
                print("fdfdfdf")
                filename = filename.decode(sys.getfilesystemencoding(), 'replace')
                return filename

            # Now to get the items according to operations defined above

            #
            # retrieve items by walking
            #
            if params.walkIt:
                maxDepth = params.walkDepth

                # remove debug only when folder renaming is fixed
                if main.debug and params.foldersOn:
                    main.recursiveFolderOn = True

                try:
                    for dirpath, dirnames, filenames in os.walk(params.root):
                        #main.Update()
                        base = dirpath.replace(params.root,'')
                        if maxDepth != 0 and len(base.split(os.path.sep)) > maxDepth:
                            continue
                        if params.filesOn:
                            for entry in filenames:
                                entry = os.path.join(base, entry)
                                filterFiles(entry)

                        # enable this when folder renaming is fixed
                        '''
                        if main.debug and params.foldersOn:
                            for entry in dirs:
                                entry = os.path.join(base,entry)
                                filterFolders(entry)
                        '''
                        main.set_status_msg(_(u"Retrieved %s items from directory")%len(files),u'wait')

                except UnicodeDecodeError as err:
                    entry = err[1].decode(sys.getfilesystemencoding(), 'replace')
                    msg = _("The item '%s' has an encoding error.\nUnable to process this path in recursive mode, please correct the name and try again.")\
                            % entry
                    utils.make_err_msg(msg, _("Unable to load item"))
                    error = True
                    pass
                except:
                    main.set_status_msg(_(u"Cannot read path!"),u'warn')
                    error = True
                    pass
                else:
                    main.set_status_msg(_(u"Retrieved %s items from directory")%len(files),u'wait')
            #
            # normal retrieval
            #
            else:
                encodingError = False
                try:
                    listedDir = os.listdir(params.root)
                except:
                    main.set_status_msg(_(u"Cannot read path!"),u'warn')
                    error = True
                    pass
                else:
                    # loop through items in directory
                    for entry in listedDir:
                        try:
                            isFolder = isDir(entry)
                        except UnicodeDecodeError:
                            entry = entry.decode(sys.getfilesystemencoding(), 'replace')
                            isFolder = isDir(entry)
                            encodingError = True
                        # load folders if set:
                        if params.foldersOn and isFolder:
                            filterFolders(entry)
                        # load files if set:
                        if params.filesOn and not isFolder:
                            filterFiles(entry)
                    if encodingError:
                        utils.make_err_msg(_("At least one item has an encoding error in its name. You will not be able to modify these."),
                        _("Encoding Error"))

            if error is not True:
                self.addItemsToPanel(folders, files)
                main.set_status_msg(_(u"Retrieved %s items from directory")%self.getItemsInPanelCount(),
                   u'complete')

                # after retrieval:
                self.enablePanelWidget('selectAll', True)
                main.menuPicker.getAllMenu.Enable(True)

            main.bottomWindow.display.DeleteAllItems()
            utils.set_busy(False)
            main.Refresh()

            # output time taken if set
            if main.show_times:
                print( "%s items load : %s"%(self.getItemsInPanelCount(), (time.time() - t)) )

            if main.prefs.get(u'autoSelectAll'):
                self.selectAllItemsInPanel()