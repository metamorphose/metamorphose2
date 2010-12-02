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

class NotebookPanel(wx.Panel):
    """
    Base class for a main operation panel in a notebook.
    i.e. insert, replace, directory
    """

    def __init__(self, main_window):
        global main
        main = main_window

    def enableNotebookTabs(self, event):
        eventObject = event.GetEventObject()
        parent = self.GetParent()

        value = eventObject.GetValue()

        if ':'+_(u"date")+':' in value or ':'+_(u"time")+':' in value :
            parent.add_datetime_page()
        else:
            parent.remove_page_by_type('datetime')

        if ':'+_("numb")+':' in value :
            parent.add_numbering_page()
        else:
            parent.remove_page_by_type('numb')
                
        main.show_preview(event)