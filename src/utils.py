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
Helper functions available throughout Metamorphose.
"""

from __future__ import print_function
import wx
import wx.html
import os
import sys
import codecs
import locale
import time
import app

try:
    import Image
except:
    pass

homedir = 'metamorphose2'
if os.sep == '/':
    homedir = '.' + homedir

def get_wxversion():
    """Get the wxPython Version."""
    wxVer = ""
    for x in wx.VERSION:
        wxVer = wxVer + str(x) + "."
    wxVer = wxVer.rstrip(".")
    return wxVer

def is_pil_loaded():
    """Determine if the python imaging library is loaded."""
    try:
        Image
    except NameError:
        return False
    else:
        return True

def set_min_size(parent, ignoreCtrls=(), ignoreClasses=()):
    """Recursively set all sizes to platform defaults
    (modified from Boa-Constructor)"""
    # need this for some cases in linux, otherwise cuts off text
    if wx.Platform == '__WXGTK__' and isinstance(parent, wx.StaticText):
        textSize = parent.GetTextExtent(parent.GetLabel())
        size = wx.Size(textSize[0]+2,-1)
    else:
        size = wx.DefaultSize

    parent.SetMinSize(size)
    parent.SetSize(size)

    for child in parent.GetChildren():
        if child not in ignoreCtrls and not isinstance(child, ignoreClasses):
            set_min_size(child, ignoreCtrls, ignoreClasses)

def adjust_exact_buttons(parent, ignore=()):
    """
    Adjust button sizes when using BU_EXACTFIT

    ignore = tuple of buttons to ignore
    """
    for child in parent.GetChildren():
        if isinstance(child, wx.Button) and child.GetName() not in ignore:
            txt = child.GetLabel()
            size = wx.Size(child.GetTextExtent(txt)[0] + 18,-1)
            child.SetMinSize(size)

def safe_makedir(dir):
    """Create a folder."""
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except OSError as error:
            if error[0] == 17:
                pass
            else:
                make_err_msg(unicode(error), u"Error")
                pass

def init_environment():
    """Create necessary folders."""
    dirs = ('undo', 'configs')
    for d in dirs:
        safe_makedir(get_user_path(d))

def calc_slice_pos(s,l):
    """Calculate the correct start and end positions for slices."""
    if s == -1 and l == 1:
        frm = -1
        to = None
    elif s < 0 and l > 1:
        frm = s#-l+1
        to = s+l
        if to >= 0:
            to = None
    else:
        frm = s
        to = s+l
    return frm,to

def make_yesno_dlg(msg, title):
    """Show a generic yes / no choice message dialog."""
    dlg = wx.MessageDialog(None, msg, title, wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)
    if dlg.ShowModal() == wx.ID_YES:
        returnValue = True
    else:
        returnValue = False
    dlg.Destroy()
    return returnValue

def make_err_msg(msg, title=None):
    """Make a generic error message dialog."""
    if not title:
        title = _(u"Error")
    dlg = wx.MessageDialog(None, msg, title, wx.ICON_ERROR)
    dlg.ShowModal()
    dlg.Destroy()

def make_warn_msg(msg, title=None):
    """Make a generic warning message dialog."""
    if not title:
        title = _(u"Warning")
    dlg = wx.MessageDialog(None, msg, title, wx.ICON_WARNING)
    dlg.ShowModal()
    dlg.Destroy()

def make_info_msg(msg, title=None):
    """Make a generic info message dialog."""
    if not title:
        title = _(u"Information")
    dlg = wx.MessageDialog(None, msg, title, wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()

def get_user_path(file):
    """Return user's default config path."""
    base = wx.StandardPaths.Get().GetUserConfigDir()
    return os.path.join(base,homedir,file)

def locale_path(lang):
    """Return locale directory."""
    # windows py2exe
    if hasattr(sys, "frozen"):
        return app.get_real_path(u'messages')
    # Linux, freeBSD when installed
    elif os.path.exists(u'/usr/share/locale/%s/LC_MESSAGES/metamorphose2.mo'%lang):
        return u'/usr/share/locale'
    # run from source
    else:
        return app.get_real_path(u'../messages')

def icon_path(icon):
    """Get the full icon path."""
    return app.get_real_path(u'icons/%s'%icon)

def add_to_warnings(main,path,msg):
    """Add an item to warnings."""
    ec = main.ec
    if main.warn.count(ec) < 1:
        main.warn.append(ec)
        main.errorLog.insert(0, (ec, path, msg, u'warn'))

def add_to_errors(main, path, msg):
    """Add an item to errors."""
    ec = main.ec
    if main.bad.count(ec) < 1:
        main.bad.append(ec)
        main.errorLog.insert(0, (ec, path, msg, u'bad'))

def reset_counter(parent, tools, c):
    """Reset a numbering counter."""
    tools.opButtonsPanel.counter = c
    tools.opButtonsPanel.auxCount = 0
    parent.numberingPanel.set_number_params(True)

def write_file(path, data):
    """Write to a file."""
    try:
        os.makedirs(os.path.dirname(path))
    except:
        pass
    try:
        fp = codecs.open(path, 'w', 'utf_8')
    except (IOError, OSError) as error:
        make_err_msg(unicode(error), _(u"Error"))
        pass
    else:
        fp.write(unicode(data))
        fp.close()

def get_notebook_page_names(parent):
    """
    Get all notebook page names.

    parent = notebook object.
    """
    pages = []
    for i in range(parent.notebook.GetPageCount()):
        pages.append(parent.notebook.GetPage(i))
    return pages

def dev_null(event):
    """
    Do nothing.
    
    Sometimes need to bind to this when programmatically doing things.
    """
    pass

def udate(main, format, itemDateTime):
    """Time encode/decode crap, a workaround for strftime not accepting unicode."""
    #print(main.encoding)
    udate = time.strftime(format.encode(main.encoding), itemDateTime)
    return udate.decode(main.encoding)

def set_busy(busy):
    """Set the application as busy, disable user input."""
    if busy:
        wx.BeginBusyCursor()
    else:
        wx.EndBusyCursor()

def get_encoding_choices(key):
    """Return valid encodings tuple for a given language type."""
    encodingLookup = {
        _(u"Use System Default") : (u"%s"%locale.getlocale()[1],),
        _(u'All Languages / Unicode') : (u'utf_8', u'utf_16'),
        _(u'Western Europe') : (u'windows-1252', u'iso-8859-1', u'iso-8859-15',
            u'mac_roman', u'cp500', u'cp850', u'cp1140'),
        _(u'Central & Eastern Europe') : (u'windows-1250', u'iso-8859-2',
            u'mac_latin2', u'cp852'),
        _(u'Esperanto, Maltese') : (u'iso-8859-3',),
        _(u'Nordic Languages') : (u'iso-8859-10', u'mac_iceland', u'cp861',
            u'cp865'),
        _(u'Celtic Languages') : (u'iso8859_14', ),
        _(u'Baltic Languages') : (u'windows-1257',u'iso-8859-13',u'cp775'),
        _(u'Cyrillic Languages') : (u'windows-1251',u'iso-8859-5',u'koi8_r',
            'koi8_u',u'mac_cyrillic',u'cp154',u'cp866',u'cp855'),
        _(u'Greek') : (u'windows-1253',u'iso-8859-7',u'mac_greek',u'cp737',
            u'cp869',u'cp875'),
        _(u'Turkish') : (u'windows-1254', u'iso-8859-9', u'mac_turkish',
            u'cp857', u'cp1026'),
        _(u'Hebrew') : (u'windows-1255', u'iso-8859-8', u'cp424', u'cp856',
            u'cp862'),
        _(u'Arabic') : (u'windows-1256', u'iso-8859-6', u'cp864'),
        _(u'Urdu') : (u'cp1006', ),
        _(u'Thai') : (u'cp874', ),
        _(u'Vietnamese') : (u'windows-1258', ),
        _(u'Traditional Chinese') : (u'ms950', u'big5hkscs', u'big5'),
        _(u'Simplified Chinese') : (u'gb2312', u'hz'),
        _(u'Unified Chinese') : (u'ms936', u'gb18030'),
        _(u'Korean') : (u'ms949', u'iso-2022-kr', u'ms1361', u'euc_kr'),
        _(u'Japanese') : (u'ms-kanji', u'iso-2022-jp', u'shift_jis', u'euc_jp',
            u'iso-2022-jp-1', u'iso-2022-jp-2004', u'iso-2022-jp-3',
            u'iso-2022-jp-ext', u'shift_jis_2004', u'shift_jisx0213',
            u'euc_jis_2004', u'euc_jisx0213'),
        }
    return encodingLookup[key]
