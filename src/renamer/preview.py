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

"""
Preview generator.

Takes user settings and generates new names based on them.
"""

from __future__ import print_function
import os
import re
import time

import app
import classes

# preview generator, should not be accesed directly
#
class Core():
    def __init__(self, MainWindow):
        global main
        main = MainWindow
        self.setup()

    # should be called before running to intialise
    def setup(self):
        self.prefs = app.prefs


    def getOperations(self):
        def getActive(x):
            if x.IsEnabled():
                return x
        return filter(getActive, main.renamer.operations)


    def addStatus(self, x):
        """Add renamed status."""
        return [x, False]


    def setStatusMessage(self):
        """Show some messages and display problems in error tab."""
        main.display_results()

        # good, no errors no warnings:
        if len(main.bad) == 0 and len(main.warn) == 0:
            if not app.REmsg:
                main.set_status_msg(_(u"Previewed %s items with no errors")\
                                    % len(main.toRename), u'complete')
        # problems:
        else:
            main.errors.show()
            # switch to error panel if set so in preferences
            if self.prefs.get(u'autoShowError'):
                main.notebook.SetSelection(3)

        # only enable 'GO' button if items have been changed, and w/o errors
        if len(main.bad) == 0:
            main.bottomWindow.go.Enable(True)
            main.menuFile.GoMenu.Enable(True)
            # auto mode rename
            if app.autoModeLevel > 1:
                main.rename_items(event=True)
        else:
            main.bottomWindow.go.Enable(False)
            main.menuFile.GoMenu.Enable(False)


    def error_check_items(self):
        """Run stand-alone error check on all items,"""
        main.bad = []
        main.warn = []
        main.errorLog = []
        main.ec = 0
        self.items_ren = []

        progressDialog = classes.ProgressDialog(main, self.prefs, main.items,
                                                _(u"Error chekcing %%% names, please wait ..."))

        for item in main.toRename:
            original = item[0][0]
            new = os.path.split(item[1][0])[1]
            newPath = os.path.split(item[1][0])[0]

            # create the new name
            renamedItem, newPath = self.errorCheck(new, original, newPath)
            newItem = os.path.join(newPath, renamedItem)
            # add to list of renamed items (for dupe checking)
            self.items_ren.append(newItem)
            main.ec += 1 # for error/warn assignment

            if progressDialog.update(main.ec) == False:
                break

        self.items_ren = map(self.addStatus, self.items_ren)
        main.toRename = zip(main.items, self.items_ren)

        progressDialog.destroy()

        self.setStatusMessage()



    #--- ERROR CHECKING: -----------------------------------------------------#
    # TODO : should be separate class within this file
    def appendErrorLog(self, ec, itemToRename, msg, log):
        if log == u'warn':
            main.warn.append(ec)
        else:
            main.bad.append(ec)
        main.errorLog.insert(0, (ec, itemToRename, msg, log))


    def errorCheck(self, renamedItem, itemToRename, path):
        """Do final error checking and optional character stripping.
        Run on each item to be renamed.
        """
        bad = main.bad
        warn = main.warn
        ec = main.ec

        #------------ ERRORS: ---------------#

        # remove os-specific path separator
        renamedItem = renamedItem.replace(unicode(os.sep), '')

        # remove or flag invalid characters (depends on user settings)
        if self.prefs.get(u'useWinChars'):
            x = 0
            for char in self.prefs.get(u'bad_chars'):
                if self.prefs.get(u'deleteBadChars'):
                    renamedItem = renamedItem.replace(char, '')
                elif self.prefs.get(u'markWarning'):
                    if x < 1 and char in renamedItem:
                        self.appendErrorLog(ec, itemToRename,
                                            _(u"Invalid Windows character: %s") % char,
                                            u'warn')
                        x += 1
                elif self.prefs.get(u'markBadChars'):
                    if x < 1 and char in renamedItem:
                        self.appendErrorLog(ec, itemToRename,
                                            _(u"Invalid Windows character: %s") % char,
                                            u'bad')
                        x += 1

        # flag bad win words:
        if self.prefs.get(u'useWinNames'):
            if self.prefs.get(u'winNamesWarn'):
                log = u'warn'
            else:
                log = u'bad'
            for word in self.prefs.get(u'bad_win_words'):
                if renamedItem.lower() == word:
                    self.appendErrorLog(ec, itemToRename,
                                        _(u"Invalid name: %s") % word, log)

        # completely blank
        if renamedItem == '' and bad.count(ec) < 1:
            self.appendErrorLog(ec, itemToRename, _(u"Completely blank"), u'bad')

        # nothing over 255 characters allowed
        elif len(renamedItem) > 255:
            #if bad.count(ec) < 1:
            self.appendErrorLog(ec, itemToRename,
                                _(u"Name length over 255 characters"), u'bad')

        # no dupes (must be last error check)
        if os.path.join(path, renamedItem) in self.items_ren:
            if ec not in bad:
                self.appendErrorLog(ec, itemToRename, _(u"Duplicate name"), u'bad')

        #------------ WARNINGS: ---------------#
        # blank file name, but extension is there
        # check original name too, to avoid flagging hidden files in *nix.
        leaf = os.path.basename(itemToRename)
        newBlank = re.search("^\..+", renamedItem)
        oldBlank = re.search("^\..+", leaf)

        if  (newBlank != None and oldBlank == None) and ec not in warn\
            and ec not in bad and os.path.isfile(itemToRename):
                self.appendErrorLog(ec, itemToRename, _(u"Blank file name"), u'warn')

        return (renamedItem, path)


    # Stop ongoing preview
    def stopPreview(self):
        main.bottomWindow.go.Enable(False)
        main.menuFile.GoMenu.Enable(False)
        main.menuFile.SaveLog.Enable(False)
        main.bottomWindow.display.DeleteAllItems()


    def generate_names(self, event):
        """
        Helping function, mainly checks various conditions to see if running
        the preview is appropriate.
        """
        #--- initial variables ---#
        run = True # load items and run preview?

        # only preview when there are operations
        operations = self.getOperations()

        if main.items == u'config_load':
            run = False
        if len(operations) == 0:
            run = False

        if run:
            # make sure we have items
            main.items = main.picker.return_sorted()
            if main.items == []:
                self.stopPreview()
            # generate preview
            else:
                for operation in operations:
                    if hasattr(operation, 'reset_counter'):
                        operation.reset_counter(0)
                self.run(operations)
        else:
            self.stopPreview()



    #--- GENERATE NEW NAMES --------------------------------------------------#

    def run(self, operations):
        """
        Parse user settings, go through each item to be renamed and apply renaming
        operations. Results are stored in the dictionary 'self.toRename' which is
        used by the rename function to rename.
        """
        main.Update()
        main.set_status_msg(_(u"Generating %s new names, please wait ...") % len(main.items), u'wait')

        if app.showTimes:
            t = time.time()

        main.counter = 0
        main.bad = []
        main.warn = []
        main.ec = 0
        main.errorLog = []
        self.items_ren = []
        app.REmsg = False # regular expression warn message

        # define here for faster processing
        def split(item):
            return os.path.split(item)
        def splitext(item):
            return os.path.splitext(item)
        def join(newPath, renamedItem):
            return unicode(os.path.join(newPath, renamedItem))

        # test for numbering panel
        hasNumbering = False
        for op in operations:
            if hasattr(op, 'numberingPanel'):
                hasNumbering = True
                break

        # set some numbering globals
        if hasNumbering:
            main.lastDir = False
            main.lastName = '\n\t\r'# no item should ever have this name!
            main.curName = False

        progressDialog = classes.ProgressDialog(main, self.prefs, main.items,
                                                _(u"Generating %%% new names, please wait ..."))

        # define here for faster access
        onlyShowChangedItems = app.prefs.get('onlyShowChangedItems')

        for itemToRename, isFile in main.items:
            # clear stuff out
            splitPath = split(itemToRename)
            newPath = splitPath[0]
            # split name & extension
            renamedItem = splitPath[1]
            if isFile:
                splitName = splitext(renamedItem)
                newName = splitName[0]
                newExt = splitName[1][1:]
            else:
                newName = renamedItem
                newExt = False

            app.debug_print(itemToRename)

            if hasNumbering: main.curDir = newPath

            # go through each operation
            for i in range(len(operations)):
                op = operations[i]

                newPath, newName, newExt = op.rename_item(newPath, newName,
                                                          newExt, itemToRename)

                if newExt is not False:
                    renamedItem = newName + '.' + newExt
                else:
                    renamedItem = newName

                # get name as it is before the last operation
                # use to reset numbering based on duplicate names
                if hasNumbering and len(operations)-2 == i:
                    main.curName = renamedItem

            renamedItem, newPath = self.errorCheck(renamedItem, itemToRename,
                                                   newPath)

            # add to list of renamed items
            newItem = join(newPath, renamedItem)
            if not onlyShowChangedItems:
                self.items_ren.append(newItem)
            elif newItem != itemToRename or main.ec in main.bad or\
                main.ec in main.warn:
                    self.items_ren.append(newItem)

            app.debug_print("%s\n" % newItem)

            # increment item position counters
            main.ec += 1 # for error/warn assignment

            if progressDialog.update(main.ec) == False:
                break

            # for reseting numbering
            if hasNumbering:
                main.lastDir = main.curDir # by directory
                main.lastName = main.curName # by name

        progressDialog.destroy()

        items_ren = map(self.addStatus, self.items_ren)

        # make new dict with original and renamed files:
        main.toRename = zip(main.items, items_ren)
        del items_ren

        main.menuFile.SaveLog.Enable(True)

        # output time taken if set
        if app.showTimes:
            print("%s items preview : %s" % (len(main.toRename), (time.time() - t)))

        self.setStatusMessage()
