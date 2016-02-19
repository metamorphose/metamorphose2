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
import os
import sys

"""
Application wide access and storage.

Some methods utility methods that make more sense
here than in the utils module.
"""


#
# Functions
#

def debug_print(msg):
    """Print debug messages to screen, if debugging is enabled."""
    if debug:
        try:
            print(msg)
        except:
            print('invalid char in msg')


def __set_real_path():
    """Set application path."""
    if hasattr(sys, "frozen"):
        path = os.path.dirname(sys.executable)
    else:
        path = False
        for path in sys.path:
            if 'metamorphose' in path:
                path = path.decode(sys.getfilesystemencoding())
                break
        if not path:
            print("Could not determine application path.\nMake sure the application is correctly installed.\n")
            sys.exit(1);
        #print(path)
    return os.path.join(path)

realPath = __set_real_path()


def get_real_path(path):
    """Return application path for file."""
    return os.path.join(realPath, path)


def locale_path(lang):
    """Return locale directory."""
    # windows py2exe
    if hasattr(sys, "frozen"):
        return get_real_path(u'messages')
    # Linux, freeBSD when installed
    elif os.path.exists(u'/usr/share/locale/%s/LC_MESSAGES/metamorphose2.mo' % lang):
        return u'/usr/share/locale'
    # run from source
    else:
        return get_real_path(u'../messages')


#
# Basic Variables
#

# home directory, for config files and such
homedir = 'metamorphose2'
if os.sep == '/':
    homedir = '.' + homedir

# Application versions
__f = open(get_real_path("version"))
version = __f.readline().strip()
prefsVersion = __f.readline().strip()
__f.close()

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

# Running in GUI or CLI mode (future)
cliMode = False

#
# Classes
#

# preferences object to be set on load
prefs = False

