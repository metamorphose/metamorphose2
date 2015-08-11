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

A professional renaming tool, it has many powerful functions.
Well suited for those that need to rename many files and/or folders on a regular basis.

In addition to general usage operations, it is useful for photo and music
collections, webmasters, programmers, legal and clerical, etc.

This is what you should run to start the program.
"""

from __future__ import print_function
import sys
import getopt
import app


syspath = sys.path[0]

if not hasattr(sys, "frozen"):
    try:
        import wxversion
    except ImportError:
        print("\nwxPython required!\n")
        sys.exit()
import os
import platform


def usage():
    """
    Print CLI usage and options to screen.
    """
    print()
    print("Metamorphose 2.%s" % app.version)
    print("Copyright (C) 2006-2015 ianare sevi")
    print("<https://github.com/metamorphose/metamorphose2>\n")
    print("Metamorphose is a graphical mass renaming program for files and folders.")
    print("There is support for automating GUI tasks via command line.\n")
    print("metamorphose2 [/path/to/open/spaces ok]")
    print("metamorphose2 [-t] [-d] [-p /path/to/open] [[-c /path/to/file.cfg] [-a level (0-3)]] [-l language]")
    print()
    print("-h,  --help       Show help screen and exit.")
    print("-t,  --timer      Show time taken to complete operations.")
    print("-d,  --debug      Show debugging information.")
    print("-p=, --path       Specify a directory to load.")
    print("-c=, --config     Specify a configuration file to load.")
    print("-a=, --auto       Specify automatic mode level to use with configuration file:")
    print("                    0 = do not preview items")
    print("                    1 = auto preview items")
    print("                    2 = auto rename items")
    print("                    3 = auto rename items and exit on success")
    print("-l=, --language   Override preferred language:")
    print("                    en_US")
    print("                    fr")
    print("                    es")
    print("-w=, --wxversion  Specify wxPython Version - use at your own risk!")
    print()
    print("If no other options are given, you may specify a path to open:")
    print("$ metamorphose2 /srv/samba/Windows Likes Spaces")
    print()
    sys.exit()


def strip_leading(a):
    """
    remove a leading '=' from CLI options
    """
    if '=' in a:
        a = a.lstrip('=')
    return a


def get_options():
    """
    Get options passed in at the command line
    """
    short_options = "htdp:vc:va:vl:vw:v"
    long_options = ["help", "timer", "debug", "path=", "config=", "auto=", "language=", "wx="]
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_options, long_options)
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    options = {
        'path': False,
        'configFilePath': False,
    }

    wx_version = '2.8'

    if sys.argv[1:] != [] and opts == []:
        options['path'] = ''
        for chunk in sys.argv[1:]:
            options['path'] += chunk + ' '

    for o, a in opts:
        if o in ("-t", "--timer"):
            app.showTimes = True
            print("Showing processing times")
        elif o in ("-d", "--debug"):
            app.debug = True
            print("Running in debug mode")
            print("Version: " + app.version)
        elif o in ("-p", "--path"):
            options['path'] = strip_leading(a)
        elif o in ("-h", "--help"):
            usage()
        elif o in ("-c", "--config"):
            options['configFilePath'] = strip_leading(a)
        elif o in ("-a", "--auto"):
            level = strip_leading(a)
            if level not in ('0', '1', '2', '3'):
                exit("Invalid auto mode level: '%s'" % level)
            elif not options['configFilePath']:
                exit("Auto mode level must be used with configuration file ( '-c' or '--config' option )")
            else:
                print("Auto mode level set: %s" % level)
                app.autoModeLevel = int(level)
        elif o in ("-l", "--language"):
            app.language = strip_leading(a)
        elif not hasattr(sys, "frozen") and o in ("-w", "--wxversion"):
            wx_version = strip_leading(a)

    if wx_version != '2.8':
        print("\nWarning: Metamorphose has only been tested on wxPython version 2.8!\n")

    return wx_version, options


def main(wx_version, cli_options):
    if platform.system() == 'Linux':
        try:
            # to fix some KDE display issues:
            del os.environ['GTK_RC_FILES']
            del os.environ['GTK2_RC_FILES']
        except (ValueError, KeyError):
            pass

    try:
        wxversion.select(wx_version)
    except wxversion.VersionError:
        print("\nFailed to load wxPython version %s!\n" % wx_version)
        sys.exit()

    import wx
    if 'unicode' not in wx.PlatformInfo:
        print("\nInstalled version: %s\nYou need a unicode build of wxPython to run Metamorphose 2.\n"
              % wxversion.getInstalled())

    # wxversion changes path
    sys.path[0] = syspath

    import MainWindow

    class BoaApp(wx.App):
        def OnInit(self):
            wx.InitAllImageHandlers()
            self.main = MainWindow.create(None, cli_options)
            self.main.Show()
            self.SetTopWindow(self.main)
            return True

    application = BoaApp(0)
    application.MainLoop()


if __name__ == '__main__':
    wx_version, cli_options = get_options()
    main(wx_version, cli_options)


