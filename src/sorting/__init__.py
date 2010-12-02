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
Sort items based on name, attribute and some support for sorting based
on file content (images, music).
"""

import utils
import classes
import sys
import os
import re
import EXIF

import wxSortingView


class Parameters(classes.Parameters):
    """Handle loading parameters"""

    def __init__(self, Panel):
        # set the picker panel
        self.Panel = Panel
        # define the operation type used to retrieve values
        self.set_value_method()

    # load all needed panel values to instance
    def load(self):
        widgets = (
            'byPosition',
            'PosStart',
            'PosLength',
            'intelySort',
            'statSort',
            'manually',
            'dirsPlace',
            'statSortChoice',
            'descending',
        )
        return self.set_parameters(widgets)


class Core():
    def __init__(self, parent, main_window):
        global main
        main = main_window

        if sys.platform == u'win32':
            self.ctime = _(u"creation time")
        else:
            self.ctime = _(u"metadata change time")

        self.Panel = wxSortingView.Panel(self, parent, main_window)
        self.params = Parameters(self.Panel)


    # Get wanted Exif info from image for sorting
    def get_from_exif(self, path, selection):
        ref = {7 : 'EXIF DateTimeOriginal', 8 : 'Image DateTime'}
        try:
            file=open(path, 'rb')
        except:
            return False
        else:
            # get the tags
            data = EXIF.process_file(file, details=False)
            if not data:
                return False
            else:
                try:
                    datetime = unicode(data[ref[selection]])
                except KeyError:
                    return False
                else:
                    datetime = datetime.replace(' ', ':')
                    return datetime


    # do the sorting on given list of items
    def sortItems(self, joinedItems):
        # load 'em up
        params = self.params.load()

        # Create sorting helper function based on user selections
        #
        # sorting by section
        if params.byPosition:
            s = params.PosStart
            l = params.PosLength
            frm,to = utils.calc_slice_pos(s,l)
            def foldersKey(x):
                return os.path.basename(x[0])[frm:to].lower()
            def filesKey(x):
                dir, file = os.path.split(x[0])
                return (dir, file[frm:to].lower())

        # inteligent number sorting
        elif params.intelySort:
            # return the number in the name
            def getNumb(x):
                try:
                    compare = float(re.sub('\D','',x[0]))
                except ValueError:
                    compare = x[0]
                return compare
            # sort by the number
            def foldersKey(x):
                return getNumb(x)
            def filesKey(x):
                compare = getNumb(x)
                return (os.path.dirname(x[0]), compare)

        # sort by item attributes
        elif params.statSort:
            selection = params.statSortChoice

            # retrieval from Exif tags
            if selection > 6:
                def foldersKey(x):
                    return 0
                def filesKey(x):
                    return self.get_from_exif(x[0], selection)

            # retrieval from os.stat
            else:
                # choices are in different order than os.stat
                ref = ('st_ctime', 'st_mtime', 'st_atime', 'st_size', 'st_mode',
                       'st_uid', 'st_gid')
                s = ref[selection]
                def foldersKey(x):
                    stat = os.stat(x[0])
                    return getattr(stat, s)
                def filesKey(x):
                    stat = os.stat(x[0])
                    return getattr(stat, s)

        # normal sorting
        else:
            def foldersKey(x):
                return x[0].lower()
            def filesKey(x):
                return (os.path.dirname(x[0]), x[0].lower())

        # Now apply created helper defs to sort
        #
        # sort items automatically
        if not params.manually:
            main.currentItem = None
            self.fc = 0
            def dirsTop(f):
                if f[1] == 0:
                    self.fc += 1
                return f[1]
            def dirsBottom(f):
                if f[1] == 0:
                    return 1
                else:
                    self.fc += 1
                    return 0

            # place directories where in list?
            if params.dirsPlace == 0:
                joinedItems.sort(key=dirsTop)
            if params.dirsPlace == 1:
                joinedItems.sort(key=dirsBottom)

            # separate files from folders
            folders = joinedItems[:self.fc]
            files = joinedItems[self.fc:]

            # sort both
            folders.sort(key=foldersKey)
            files.sort(key=filesKey)

            # join back together
            joinedItems[:self.fc] = folders
            joinedItems[self.fc:] = files

            # reverse sort list?
            if params.descending:
                joinedItems.reverse()

        return joinedItems