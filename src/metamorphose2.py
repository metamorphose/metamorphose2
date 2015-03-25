#!/usr/bin/env python
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
#
# All translations also Copyright (c) Ianaré Sévi, under the BSD license
#

"""
Métamorphose is a free, open source program to mass rename files and folders.

A profesional renaming tool, it has many powerful functions.
Well suited for those that need to rename many files and/or folders on a regular basis.

In addition to general usage operations, it is useful for photo and music
collections, webmasters, programmers, legal and clerical, et cetera.

This is what you should run to start the program.
"""

from __future__ import print_function
import sys
path = sys.path[0]

# Prefer wxpython 2.8
if not hasattr(sys, "frozen"):
    msg = "\nwxPython 2.8 is required!\n"
    try:
        import wxversion
    except:
        print(msg)
        sys.exit()
    else:
        try:
            wxversion.select('2.8')
        except:
            print(msg)
            sys.exit()
import wx
import os
import platform
import MainWindow

# wxversion changes path
sys.path[0] = path

class BoaApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        self.main = MainWindow.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True


def main():
    if platform.system() == 'Linux':
        try:
            # to fix some KDE display issues:
            del os.environ['GTK_RC_FILES']
            del os.environ['GTK2_RC_FILES']
        except (ValueError, KeyError):
            pass

    application = BoaApp(0)
    application.MainLoop()


if __name__ == '__main__':
    if 'unicode' not in wx.PlatformInfo:
        print("\nInstalled version: %s\nYou need a unicode build of wxPython to run Metamorphose 2.\n"
              % wxversion.getInstalled())
    else:
        main()
