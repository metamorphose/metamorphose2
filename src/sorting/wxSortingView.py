# -*- coding: utf-8 -*-
#Boa:FramePanel:sortingPanel

# Copyright (C) 2006-2013 ianaré sévi <ianare@gmail.com>
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
import wx

[wxID_SORTINGPANEL, wxID_SORTINGPANELADVANCEDBOX, wxID_SORTINGPANELASCENDING,
    wxID_SORTINGPANELBASICBOX, wxID_SORTINGPANELBYPOSITION,
    wxID_SORTINGPANELDESCENDING, wxID_SORTINGPANELDIRSPLACE,
    wxID_SORTINGPANELDOWNBOTTOM, wxID_SORTINGPANELDOWNBUTTON,
    wxID_SORTINGPANELDOWNMORE, wxID_SORTINGPANELINTELYSORT,
    wxID_SORTINGPANELMANUALLY, wxID_SORTINGPANELPOSLENGTH,
    wxID_SORTINGPANELPOSSTART, wxID_SORTINGPANELSTATICTEXT1,
    wxID_SORTINGPANELSTATICTEXT2, wxID_SORTINGPANELSTATSORT,
    wxID_SORTINGPANELSTATSORTCHOICE, wxID_SORTINGPANELUPBUTTON,
    wxID_SORTINGPANELUPMORE, wxID_SORTINGPANELUPTOP,
    wxID_SORTINGPANELNORMALSORT,
] = [wx.NewId() for __init_ctrls in range(22)]

class Panel(wx.Panel):
    def __init_mainsizer_items(self, parent):
        parent.AddSizer(self.staticBoxSizer1, 0, border=20, flag=wx.ALL)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=wx.ALL)
        parent.AddSizer(self.staticBoxSizer2, 0, border=20, flag=wx.ALL)

    def _init_coll_byPosSixer_items(self, parent):
        parent.AddWindow(self.staticText1, 0, border=20,
                         flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT)
        parent.AddWindow(self.PosStart, 0, border=4, flag=wx.LEFT)
        parent.AddWindow(self.staticText2, 0, border=10,
                         flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT)
        parent.AddWindow(self.PosLength, 0, border=4, flag=wx.LEFT)

    def _init_coll_buttonSizer_items(self, parent):
        parent.AddWindow(self.upButton, 0, border=5, flag=wx.LEFT)
        parent.AddWindow(self.downButton, 0, border=4, flag=wx.LEFT)
        parent.AddWindow(self.upMore, 0, border=8, flag=wx.LEFT)
        parent.AddWindow(self.downMore, 0, border=4, flag=wx.LEFT)
        parent.AddWindow(self.upTop, 0, border=8, flag=wx.LEFT)
        parent.AddWindow(self.downBottom, 0, border=4, flag=wx.LEFT)

    def _init_coll_staticBoxSizer1_items(self, parent):
        parent.AddWindow(self.ascending, 0, border=5, flag=wx.ALL)
        parent.AddWindow(self.descending, 0, border=5, flag=wx.ALL)
        parent.AddWindow(self.manually, 0, border=5, flag=wx.ALL)
        parent.AddSizer(self.buttonSizer, 0, border=15, flag=wx.RIGHT | wx.LEFT)
        parent.AddSpacer(wx.Size(10, 10), border=5, flag=0)
        parent.AddWindow(self.dirsPlace, 0, border=5, flag=wx.ALL)

    def _init_coll_staticBoxSizer2_items(self, parent):
        parent.AddWindow(self.normalSort, 0, border=5, flag=wx.ALL)
        parent.AddWindow(self.intelySort, 0, border=5, flag=wx.ALL)
        parent.AddWindow(self.byPosition, 0, border=5, flag=wx.ALL)
        parent.AddSizer(self.byPosSixer, 0, border=5,
                        flag=wx.BOTTOM | wx.RIGHT | wx.LEFT)
        parent.AddWindow(self.statSort, 0, border=5, flag=wx.ALL)
        parent.AddWindow(self.statSortChoice, 0, border=25, flag=wx.LEFT)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)

    def __init_sizers(self):
        self.mainSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.buttonSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.byPosSixer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.staticBoxSizer1 = wx.StaticBoxSizer(box=self.basicBox,
                                                 orient=wx.VERTICAL)
        self.staticBoxSizer2 = wx.StaticBoxSizer(box=self.advancedBox,
                                                 orient=wx.VERTICAL)
        self.__init_mainsizer_items(self.mainSizer)
        self._init_coll_buttonSizer_items(self.buttonSizer)
        self._init_coll_byPosSixer_items(self.byPosSixer)
        self._init_coll_staticBoxSizer1_items(self.staticBoxSizer1)
        self._init_coll_staticBoxSizer2_items(self.staticBoxSizer2)
        self.SetSizer(self.mainSizer)

    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_SORTINGPANEL, name=u'sortingPanel',
                          parent=prnt, style=wx.TAB_TRAVERSAL)

        self.basicBox = wx.StaticBox(id=wxID_SORTINGPANELBASICBOX,
                                     label=_(u"Basic Options"), name=u'basicBox', parent=self,
                                     style=0)

        self.advancedBox = wx.StaticBox(id=wxID_SORTINGPANELADVANCEDBOX,
                                        label=_(u"Advanced Options"), name=u'advancedBox', parent=self,
                                        style=0)

        self.ascending = wx.RadioButton(id=wxID_SORTINGPANELASCENDING,
                                        label=_("Ascending (0 - 9)"), name='ascending', parent=self,
                                        style=wx.RB_GROUP)
        self.ascending.Bind(wx.EVT_RADIOBUTTON, self.setSortingOptions,
                            id=wxID_SORTINGPANELASCENDING)

        self.descending = wx.RadioButton(id=wxID_SORTINGPANELDESCENDING,
                                         label=_("Descending (9 - 0)"), name='descending', parent=self,
                                         style=0)
        self.descending.Bind(wx.EVT_RADIOBUTTON, self.setSortingOptions,
                             id=wxID_SORTINGPANELDESCENDING)

        self.manually = wx.RadioButton(id=wxID_SORTINGPANELMANUALLY,
                                       label=_(u"Manually Adjust"), name=u'manually', parent=self,
                                       style=0)
        self.manually.SetValue(False)
        self.manually.Bind(wx.EVT_RADIOBUTTON, self.setSortingOptions,
                           id=wxID_SORTINGPANELMANUALLY)

        self.downButton = wx.BitmapButton(bitmap=wx.Bitmap(utils.icon_path(u'down.png'),
                                          wx.BITMAP_TYPE_PNG), id=wxID_SORTINGPANELDOWNBUTTON,
                                          name=u'downButton', parent=self, style=wx.BU_AUTODRAW)
        self.downButton.Bind(wx.EVT_BUTTON, self.change_item_order,
                             id=wxID_SORTINGPANELDOWNBUTTON)

        self.upButton = wx.BitmapButton(bitmap=wx.Bitmap(utils.icon_path(u'up.png'),
                                        wx.BITMAP_TYPE_PNG), id=wxID_SORTINGPANELUPBUTTON,
                                        name=u'upButton', parent=self, style=wx.BU_AUTODRAW)
        self.upButton.Bind(wx.EVT_BUTTON, self.change_item_order,
                           id=wxID_SORTINGPANELUPBUTTON)

        self.upTop = wx.BitmapButton(bitmap=wx.Bitmap(utils.icon_path(u'upAll.ico'),
                                     wx.BITMAP_TYPE_ICO), id=wxID_SORTINGPANELUPTOP, name=u'upTop',
                                     parent=self, style=wx.BU_AUTODRAW)
        self.upTop.SetToolTipString(_(u"move to top"))
        self.upTop.Bind(wx.EVT_BUTTON, self.change_item_order,
                        id=wxID_SORTINGPANELUPTOP)

        self.downBottom = wx.BitmapButton(bitmap=wx.Bitmap(utils.icon_path(u'downAll.ico'),
                                          wx.BITMAP_TYPE_ICO), id=wxID_SORTINGPANELDOWNBOTTOM,
                                          name=u'downBottom', parent=self, style=wx.BU_AUTODRAW)
        self.downBottom.SetToolTipString(_(u"move to bottom"))
        self.downBottom.Bind(wx.EVT_BUTTON, self.change_item_order,
                             id=wxID_SORTINGPANELDOWNBOTTOM)

        self.upMore = wx.BitmapButton(bitmap=wx.Bitmap(utils.icon_path(u'up5.png'),
                                      wx.BITMAP_TYPE_PNG), id=wxID_SORTINGPANELUPMORE, name=u'upMore',
                                      parent=self, style=wx.BU_AUTODRAW)
        self.upMore.SetToolTipString(_(u"move by 5"))
        self.upMore.Bind(wx.EVT_BUTTON, self.change_item_order,
                         id=wxID_SORTINGPANELUPMORE)

        self.downMore = wx.BitmapButton(bitmap=wx.Bitmap(utils.icon_path(u'down5.png'),
                                        wx.BITMAP_TYPE_PNG), id=wxID_SORTINGPANELDOWNMORE,
                                        name=u'downMore', parent=self, style=wx.BU_AUTODRAW)
        self.downMore.SetToolTipString(_(u"move by 5"))
        self.downMore.Bind(wx.EVT_BUTTON, self.change_item_order,
                           id=wxID_SORTINGPANELDOWNMORE)

        self.dirsPlace = wx.Choice(choices=[_(u"Directories before files"),
                                   _(u"Directories after files"),
                                   _(u"Directories mixed with files")],
                                   id=wxID_SORTINGPANELDIRSPLACE, name=u'dirsPlace', parent=self)
        self.dirsPlace.SetSelection(0)
        self.dirsPlace.Bind(wx.EVT_CHOICE, self.show_preview)

        self.normalSort = wx.RadioButton(id=wxID_SORTINGPANELNORMALSORT,
                                         label=_(u"Sort normally"), name=u'normalSort',
                                         parent=self, style=wx.RB_GROUP)
        self.normalSort.SetToolTipString(_(u"Standard sorting by item name."))
        self.normalSort.SetValue(True)
        self.normalSort.Bind(wx.EVT_RADIOBUTTON, self.setSortingOptions,
                             id=wxID_SORTINGPANELNORMALSORT)

        self.intelySort = wx.RadioButton(id=wxID_SORTINGPANELINTELYSORT,
                                         label=_(u"Sort numbers intelligently"), name=u'intelySort',
                                         parent=self, style=0)
        self.intelySort.SetToolTipString(_(u"Order these types of items: ...19, 2, 20...\nMay have unpredictable results!"))
        self.intelySort.Bind(wx.EVT_RADIOBUTTON, self.setStatOptions,
                             id=wxID_SORTINGPANELINTELYSORT)

        self.byPosition = wx.RadioButton(id=wxID_SORTINGPANELBYPOSITION,
                                         label=_(u"Sort on a section of the name:"), name=u'byPosition',
                                         parent=self, style=0)
        self.byPosition.Bind(wx.EVT_RADIOBUTTON, self.setStatOptions,
                             id=wxID_SORTINGPANELBYPOSITION)

        self.staticText1 = wx.StaticText(id=wxID_SORTINGPANELSTATICTEXT1,
                                         label=_(u"Starting at:"), name='staticText1', parent=self,
                                         style=0)

        self.PosStart = wx.SpinCtrl(id=wxID_SORTINGPANELPOSSTART, initial=0,
                                    max=255, min=-255, name=u'PosStart', parent=self, size=wx.Size(50,
                                    -1), style=wx.SP_ARROW_KEYS, value='0')
        self.PosStart.Bind(wx.EVT_SPINCTRL, self.show_preview,
                           id=wxID_SORTINGPANELPOSSTART)

        self.staticText2 = wx.StaticText(id=wxID_SORTINGPANELSTATICTEXT2,
                                         label=_(u"Selection length:"), name='staticText2', parent=self,
                                         style=0)

        self.PosLength = wx.SpinCtrl(id=wxID_SORTINGPANELPOSLENGTH, initial=1,
                                     max=255, min=1, name=u'PosLength', parent=self, size=wx.Size(50,
                                     -1), style=wx.SP_ARROW_KEYS, value='1')
        self.PosLength.Bind(wx.EVT_SPINCTRL, self.show_preview,
                            id=wxID_SORTINGPANELPOSLENGTH)

        self.statSortChoice = wx.Choice(choices=[self.ctime,
                                        _(u"last modification time"), _(u"last access time"),
                                        _(u"file size"), _(u"mode (protection bits)"),
                                        _(u"user ID of owner"), _(u"group ID of owner"),
                                        _(u"Exif : picture taken"),
                                        _(u"Exif : image modified"),
                                        ],
                                        id=wxID_SORTINGPANELSTATSORTCHOICE, name=u'statSortChoice',
                                        parent=self, style=0)
        self.statSortChoice.SetSelection(0)
        self.statSortChoice.Bind(wx.EVT_CHOICE, self.show_preview,
                                 id=wxID_SORTINGPANELSTATSORTCHOICE)

        self.statSort = wx.RadioButton(id=wxID_SORTINGPANELSTATSORT,
                                       label=_(u"Sort by item attributes, using:"), name=u'statSort',
                                       parent=self, style=0)
        self.statSort.Bind(wx.EVT_RADIOBUTTON, self.setStatOptions,
                           id=wxID_SORTINGPANELSTATSORT)

        self.__init_sizers()


    def __init__(self, Core, parent, main_window):
        global main
        main = main_window

        self.ctime = Core.ctime

        self.__init_ctrls(parent)

        self.posOptions = (self.staticText1, self.staticText2, self.PosStart,
                           self.PosLength)
        self.setSortingOptions(False)


    # Adjust after loading config
    def on_config_load(self, ):
        self.setSortingOptions(False)

    # triggered when a button to change item position is clicked
    def change_item_order(self, event):
        buttons = {
            wxID_SORTINGPANELUPBUTTON: -1,
            wxID_SORTINGPANELDOWNBUTTON: 1,
            wxID_SORTINGPANELUPMORE: -5,
            wxID_SORTINGPANELDOWNMORE: 5,
            wxID_SORTINGPANELUPTOP: u'top',
            wxID_SORTINGPANELDOWNBOTTOM: u'bottom',
            }
        change = buttons[event.GetId()]
        main.change_item_order(change)

    def setPositionOptions(self, event):
        if self.byPosition.GetValue():
            allow = True
        else:
            allow = False
        for obj in (self.staticText1, self.PosStart, self.staticText2,
                    self.PosLength):
            obj.Enable(allow)
        main.show_preview(event)

    def setStatOptions(self, event):
        if self.statSort.GetValue():
            self.statSortChoice.Enable(True)
            for item in self.posOptions:
                item.Enable(False)
        else:
            self.statSortChoice.Enable(False)
            self.setPositionOptions(event)
        self.show_preview(event)

    # enables/disables item position change buttons:
    def setSortingOptions(self, event):
        sortButtons = (self.upButton, self.downButton,
                       self.upMore, self.downMore, self.upTop,
                       self.downBottom, )
        sortOptions = (self.dirsPlace, self.intelySort, self.byPosition)
        timeSort = (self.statSort, self.statSortChoice)

        if self.manually.GetValue():
            for item in sortButtons:
                item.Enable(True)
            for item in sortOptions:
                item.Enable(False)
            for item in self.posOptions:
                item.Enable(False)
            for item in timeSort:
                item.Enable(False)
            self.show_preview(event)
        else:
            for item in sortButtons:
                item.Enable(False)
            for item in sortOptions:
                item.Enable(True)
            self.statSort.Enable(True)
            self.setStatOptions(event)


    def show_preview(self, event):
        main.show_preview(event)

    def setTimeOptions(self, event):
        event.Skip()
