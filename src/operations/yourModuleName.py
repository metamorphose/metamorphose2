# -*- coding: utf-8 -*-

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
Example Module.
"""

from operation import Operation
import wx

[wxID_PANEL, wxID_PANELSTATICTEXT1] = [wx.NewId() for __init_ctrls in range(2)]

class OpPanel(Operation):
    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_PANEL, name=u'Panel', parent=prnt,
						  style=wx.TAB_TRAVERSAL)

        self.staticText1 = wx.StaticText(id=wxID_PANELSTATICTEXT1,
										 label=_(u"This is a translated string"), name=u'staticText1', parent=self,
										 pos=wx.Point(192, 72), size=wx.Size(-1, -1), style=0)


    def __init__(self, parent, main_window, params={}):
        Operation.__init__(self, params)
        global main
        main = main_window
        self.__init_ctrls(parent)

    # the renaming function
    def rename_item(self, path, name, ext, original):
        newName = self.join_ext(name, ext)
        if not newName:
            return path, name, ext

        #== your code START ====================#

        newName = u"it worked!"

        #== your code END ======================#

        # apply to name and/or ext
        name, ext = self.split_ext(newName, name, ext)

        return path, name, ext
