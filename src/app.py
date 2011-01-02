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

import utils

"""
Application wide access and storage.

Some methods utility methods that make more sense
here than in the utils module.
"""

# Variables

# Application version
version = utils.get_version()
# Interface language
language = ''
# Items with warnings
warn = []
# Items with errors
bad = []
# All errors
errorLog = []
# Items to rename
items = []
# Has regular expression error message
REmsg = False
# If true, will need to sort items before renaming
recursiveFolderOn = False
# Automatic mode level
autoModeLevel = False
# Show processing times
showTimes = False
# Show debug info
debug = False
# Font parameters
fontParams = {}

# Objects

# preferences object to be set on load
prefs = False


# Links


# Methods

def debug_print(msg):
    """Print debug messages to screen, if debugging is enabled."""
    if debug:
        try:
            print(msg)
        except:
            print('invalid char in msg')