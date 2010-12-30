# -*- coding: utf-8 -*-
#
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

"""Important variables needed throughout the application classes."""

version = False
warn = [] # warnings
bad = [] # errors
errorLog = [] # all errors go here
items = [] # items to rename
spacer = u" " * 6 # spacer for status messages (to clear image)
REmsg = False # regular expression error
recursiveFolderOn = False # if true, will need to sort items before renaming
language = '' # to be set later
prefs = {} # preferences, to be set later
autoModeLevel = False # automatic mode level
show_times = False # show processing times
debug = False # show debug info
