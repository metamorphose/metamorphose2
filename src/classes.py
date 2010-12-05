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

"""Base classes used throughout the application."""

import os
import wx
import utils

class Parameters:
    """Load parameters from GUI to core."""
    def set_value_method(self):
        self.get_value = self.get_wx_value

    # get a wxWidget value
    def get_wx_value(self, widget):
        if isinstance(widget, wx.ComboBox):
            value = widget.GetStringSelection()
            # inconsistences in library requires this
            if not value:
                value = widget.GetValue()
        elif isinstance(widget, wx.Choice):
            value = widget.GetSelection()
        else:
            value = widget.GetValue()
        return value

    # set given widgets
    def set_parameters(self, widgets):
        for widgetName in widgets:
            if hasattr(self.view, widgetName):
                widget = getattr(self.view, widgetName)
                setattr(self, widgetName, self.get_value(widget))
        return self


# display single page help dialog
class SmallHelp(wx.Dialog):

    def __init__(self, prnt, main, helpFile, title, icon, size=False):

        if size == False:
            size = wx.Size(610, 531)
        wx.Dialog.__init__(self, id=-1, name='smallHelpDialog', parent=prnt,
              size=size,
              style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX, title=title)
        self.SetIcon(wx.Icon(utils.get_real_path(u'icons/%s.ico')%icon,wx.BITMAP_TYPE_ICO))

        self.display = wx.html.HtmlWindow(id=-1,
              name=u'display', parent=self, style=wx.html.HW_SCROLLBAR_AUTO)

        self.Center(wx.HORIZONTAL|wx.VERTICAL)

        if u'gtk2' in wx.PlatformInfo:
            self.display.SetStandardFonts()

        docspath = utils.get_real_path(u'help')

        if os.path.isfile(os.path.join(docspath,main.language,helpFile)):
            helpFile = os.path.join(docspath,main.language,helpFile)
        else:
            helpFile = os.path.join(docspath,u'en_US',helpFile)

        self.display.LoadPage(helpFile)


# progress dialog handling
class ProgressDialog(wx.ProgressDialog):
    def __init__(self, parent, prefs, items, message):
        
        if type(items) is not type(1):
            items = len(items)
        message = message.replace(u'%%%', unicode(items))

        if prefs.get('showProgressDialog') and items > int(prefs.get(u'itemCountForProgDialog')):
            self.active = True
            wx.ProgressDialog.__init__(self,
                                       _(u"Progress"),
                                       message,
                                       maximum = items,
                                       parent=parent,
                                       style =  wx.PD_APP_MODAL
                                        | wx.PD_ELAPSED_TIME
                                        | wx.PD_AUTO_HIDE
                                        | wx.PD_CAN_ABORT
                                       )
        else:
            self.active = False

    def update(self, c):
        if self.active:
            (keepGoing, skip) = self.Update(c)
            return keepGoing

    def destroy(self):
        if self.active:
            self.Destroy()
            self = False
