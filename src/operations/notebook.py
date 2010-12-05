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


import wx
import numbering
import dateTime
import utils

class Notebook(wx.Notebook):
    """Base class for all notebooks used to display operation tabs."""

    tabs = {}
    """tabs in use"""

    def __init__(self, parent, main_window):
        global main
        main = main_window
        wx.Notebook.__init__(self, id=-1, name=u'notebook', parent=parent,
            style=wx.NB_BOTTOM|wx.NO_BORDER)
        self.SetThemeEnabled(True)
        self.numbering = numbering.Panel(self, main)
        self.dateTime = dateTime.Panel(self, main)

    def init_pages(self, varPanel, varText, varIcon):
        """initialize notebook pages"""

        # load and assign notebook page images
        il = wx.ImageList(16, 16)
        img0 = il.Add(wx.Bitmap(utils.icon_path(varIcon), wx.BITMAP_TYPE_ICO))
        img1 = il.Add(wx.Bitmap(utils.icon_path(u'numbering.ico'), wx.BITMAP_TYPE_ICO))
        img2 = il.Add(wx.Bitmap(utils.icon_path(u'date_time.ico'), wx.BITMAP_TYPE_ICO))
        self.AssignImageList(il)

        # required to make XP theme better:
        self.SetBackgroundColour(main.notebook.GetThemeBackgroundColour())

        self.AddPage(page=varPanel, text=varText, select=True,
              imageId=img0)
        self.AddPage(imageId=img1, page=self.numbering, select=False,
              text=_(u"Numbering settings"))
        self.AddPage(imageId=img2, page=self.dateTime, select=False,
                  text=_(u"Date && Time settings"))

