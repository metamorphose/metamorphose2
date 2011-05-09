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
Sort items based on name, attribute and some support for sorting based
on file content (images, music).
"""

import os
import re
import sys

import EXIF
import classes
import utils
import wxSortingView


class Parameters(classes.Parameters):
    """Handle loading parameters"""

    def __init__(self, Panel):
        self.view = Panel
        # define the operation type used to retrieve values
        self.set_value_method()

    def load(self):
        """Load all needed panel values to instance."""
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

        self.view = wxSortingView.Panel(self, parent, main_window)
        self.params = Parameters(self.view)


    def _get_from_exif(self, path, selection):
        """Get wanted Exif info from image for sorting."""
        ref = {7: 'EXIF DateTimeOriginal', 8: 'Image DateTime'}
        try:
            file = open(path, 'rb')
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

    def sort_items(self, joinedItems):
        """Sorting the given list of items."""
        # load 'em up
        params = self.params.load()

        # Create sorting helper function based on user selections
        #
        # sorting by section
        if params.byPosition:
            s = params.PosStart
            l = params.PosLength
            frm, to = utils.calc_slice_pos(s, l)
            def _folder_key(x):
                return os.path.basename(x[0])[frm:to].lower()
            def _files_key(x):
                dir, file = os.path.split(x[0])
                return (dir, file[frm:to].lower())

        # inteligent number sorting
        elif params.intelySort:
            # return the number in the name
            def _get_numb(x):
                try:
                    compare = float(re.sub('\D', '', x[0]))
                except ValueError:
                    compare = x[0]
                return compare
            # sort by the number
            def _folder_key(x):
                return _get_numb(x)
            def _files_key(x):
                compare = _get_numb(x)
                return (os.path.dirname(x[0]), compare)

        # sort by item attributes
        elif params.statSort:
            selection = params.statSortChoice

            # retrieval from Exif tags
            if selection > 6:
                def _folder_key(x):
                    return 0
                def _files_key(x):
                    return self._get_from_exif(x[0], selection)

            # retrieval from os.stat
            else:
                # choices are in different order than os.stat
                ref = ('st_ctime', 'st_mtime', 'st_atime', 'st_size', 'st_mode',
					   'st_uid', 'st_gid')
                s = ref[selection]
                def _folder_key(x):
                    stat = os.stat(x[0])
                    return getattr(stat, s)
                def _files_key(x):
                    stat = os.stat(x[0])
                    return getattr(stat, s)

        # normal sorting
        else:
            def _folder_key(x):
                return x[0].lower()
            def _files_key(x):
                return (os.path.dirname(x[0]), x[0].lower())

        # Now apply created helper defs to sort
        #
        # sort items automatically
        if not params.manually:
            main.currentItem = None
            self.fc = 0
            def _dirs_top(f):
                if f[1] == 0:
                    self.fc += 1
                return f[1]
            def _dirs_bottom(f):
                if f[1] == 0:
                    return 1
                else:
                    self.fc += 1
                    return 0

            # place directories where in list?
            if params.dirsPlace == 0:
                joinedItems.sort(key=_dirs_top)
            if params.dirsPlace == 1:
                joinedItems.sort(key=_dirs_bottom)

            # separate files from folders
            folders = joinedItems[:self.fc]
            files = joinedItems[self.fc:]

            # sort both
            folders.sort(key=_folder_key)
            files.sort(key=_files_key)

            # join back together
            joinedItems[:self.fc] = folders
            joinedItems[self.fc:] = files

            # reverse sort list?
            if params.descending:
                joinedItems.reverse()
        return joinedItems
