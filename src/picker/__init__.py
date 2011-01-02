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

"""
Selects and deselects items based on user input.
Supports direct selection, regular expression filters, and attribute filters.
"""

from __future__ import print_function
import app
import utils
import classes
import sys
import os
import re
import sre_constants
import time
import wxPickerView


class Parameters(classes.Parameters):
    """Handle loading of parameters."""
    
    def __init__(self, Panel):
        # set the picker panel
        self.view = Panel
        # define the operation type used to retrieve values
        self.set_value_method()

    def load(self):
        """Load all needed panel values to instance."""

        root = self.get_value(self.view.path)
        self.set_root_path(root)
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

    def set_root_path(self, root):
        """Load all needed panel values to instance."""
        utils.debug_print("Examining : %s"%root)
        
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

        self.view = wxPickerView.Panel(self, parent, MainWindow)
        self.params = Parameters(self.view)
        self.joinedItems = []


    # wrappers to acces Panel

    def set_status_msg(self, msg, ico):
        main.set_status_msg(msg, ico)

    def add_items_to_panel(self, folders, files):
        self.view.ItemList.add_items(self.params.root, folders, files)

    def count_panel_items(self):
        return self.view.ItemList.GetItemCount()

    def select_all(self, event=True):
        self.view.select_all(event)

    def select_none(self, event=True):
        self.view.select_none(event)

    def browse_for_path(self, event=True):
        self.view.browse_for_path(event)

    def walk_from_menu(self, event):
        self.view.walk_from_menu()
        self.refresh(True)

    def enable_panel_widget(self, widget, state):
        getattr(self.view, widget).Enable(state)

    def remove_all_items(self):
        self.view.ItemList.DeleteAllItems()

    def set_path(self, event):
        self.view.set_path(event)
        self.refresh(True)

    def enable_buttons(self):
        self.view.enable_buttons()

    def set_tree(self):
        self.view.set_tree()


    # helpers

    def clear_joined_items(self):
        self.joinedItems = []

    def return_sorted(self):
        return main.sorting.sort_items(self.joinedItems)

    def clear_all(self):
        self.clear_joined_items()
        self.remove_all_items()

    def refresh_dir_tree(self):
        if app.prefs.get(u'useDirTree'):
            self.view.refresh_dirpicker()

    def remove_items_by_name(self, itemNames):
    	for name in itemNames:
            displayedName = name.replace(self.params.root, '')
            if os.path.split(displayedName)[0] == os.sep:
                displayedName = displayedName[1:]
            self.view.remove_item_by_name(displayedName)

            # remove from item list
            IsFile = os.path.isfile(name)
            fullItem = [name, IsFile]
            self.joinedItems.remove(fullItem)
            
            self.enable_buttons()


    def _set_initial(self):
        self.clear_all()
        app.recursiveFolderOn = False
        utils.set_busy(True)
        self.enable_panel_widget('selectNone', False)
        main.menuPicker.getNoneMenu.Enable(False)
        main.bottomWindow.go.Enable(False)

    def _get_filter(self, params):
        """Get the filter used when loading items from selected directory."""
        filterSel = params.FilterSel

        # are we using a built in filter ?
        if filterSel != '' and self.view.get_in_searches(filterSel):
            filter = self.view.get_in_searches(filterSel)
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
                app.REmsg = True
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
            self.clear_all()
        # OK, load items up:
        else:
            self._set_initial()

            main.set_status_msg(_(u"Getting directory contents please wait ..."),u'wait')

            if app.showTimes:
                t = time.time()

            filter, useRE = self._get_filter(params)

            # create the search (filtering) operations ...
            notType = params.notType

            # normal filtering:
            if filter and not useRE:
                def _filter_folders(entry):
                    if filter in entry.lower() and not notType:
                        folders.append(entry)
                    if filter not in entry.lower() and notType:
                        folders.append(entry)
                def _filter_files(entry):
                    if filter in entry.lower() and not notType:
                        files.append(entry)
                    if filter not in entry.lower() and notType:
                        files.append(entry)
            # regular expression filtering
            elif filter and useRE:
                def _filter_folders(entry):
                    if filter.search(entry) and not notType:
                        folders.append(entry)
                    if not filter.search(entry) and notType:
                        folders.append(entry)
                def _filter_files(entry):
                    if filter.search(entry) and not notType:
                        files.append(entry)
                    if not filter.search(entry) and notType:
                        files.append(entry)
            # no filtering:
            else:
                def _filter_folders(entry):
                    folders.append(entry)
                def _filter_files(entry):
                    files.append(entry)

            # define here for speed boost
            def isdir(entry):
                    join = os.path.join(params.root, entry)
                    return os.path.isdir(join)

            def get_encoded_name(filename):
                filename = filename.decode(sys.getfilesystemencoding(), 'replace')
                return filename

            # Now to get the items according to operations defined above

            # retrieve items by walking
            if params.walkIt:
                maxDepth = params.walkDepth

                # remove debug only when folder renaming is fixed
                if app.debug and params.foldersOn:
                    app.recursiveFolderOn = True

                try:
                    for dirpath, dirnames, filenames in os.walk(params.root):
                        #main.Update()
                        base = dirpath.replace(params.root,'')
                        if maxDepth != 0 and len(base.split(os.path.sep)) > maxDepth:
                            continue
                        if params.filesOn:
                            for entry in filenames:
                                entry = os.path.join(base, entry)
                                _filter_files(entry)

                        # enable this when folder renaming is fixed
                        '''
                        if app.debug and params.foldersOn:
                            for entry in dirs:
                                entry = os.path.join(base,entry)
                                _filter_folders(entry)
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
            # normal retrieval
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
                            isFolder = isdir(entry)
                        except UnicodeDecodeError:
                            entry = entry.decode(sys.getfilesystemencoding(), 'replace')
                            isFolder = isdir(entry)
                            encodingError = True
                        # load folders if set:
                        if params.foldersOn and isFolder:
                            _filter_folders(entry)
                        # load files if set:
                        if params.filesOn and not isFolder:
                            _filter_files(entry)
                    if encodingError:
                        utils.make_err_msg(_("At least one item has an encoding error in its name. You will not be able to modify these."),
                        _("Encoding Error"))

            if error is not True:
                self.add_items_to_panel(folders, files)
                main.set_status_msg(_(u"Retrieved %s items from directory")%self.count_panel_items(),
                   u'complete')

                # after retrieval:
                self.enable_panel_widget('selectAll', True)
                main.menuPicker.getAllMenu.Enable(True)

            main.bottomWindow.display.DeleteAllItems()
            utils.set_busy(False)
            main.Refresh()

            # output time taken if set
            if app.showTimes:
                print( "%s items load : %s"%(self.count_panel_items(), (time.time() - t)) )

            if app.prefs.get(u'autoSelectAll'):
                self.select_all()
