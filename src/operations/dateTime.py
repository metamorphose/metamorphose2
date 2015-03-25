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

import sys

import app
import wx
import wx.calendar
import wx.lib.masked.timectrl

[wxID_PANEL, wxID_PANELCAL, wxID_PANELDATESEPERATOR,
    wxID_PANELDATETESTDISPLAY, wxID_PANELDATE_FORMAT,
    wxID_PANELGETFROMITEM,
    wxID_PANELITEMTIMETYPE, wxID_PANELSETTIMENOW,
    wxID_PANELSPIN1, wxID_PANELSTATICBOX1,
    wxID_PANELSTATICBOX2, wxID_PANELTIME_FORMAT,
    wxID_PANELSTATICTEXT1, wxID_PANELSTATICTEXT2,
    wxID_PANELSTATICTEXT3, wxID_PANELSTATICTEXT4,
    wxID_PANELSTATICTEXT5, wxID_PANELSTATICTEXT6,
    wxID_PANELTIME, wxID_PANELTIMESEPERATOR,
    wxID_PANELTIMETESTDISPLAY,
] = [wx.NewId() for __init_ctrls in range(21)]

class Panel(wx.Panel):
    """
    The date and time panel in a notebook operation.
    """

    def __init_sizer(self):
        topRow = wx.BoxSizer(wx.HORIZONTAL)
        topRow.Add((15, -1), 0)
        topRow.Add(self.getFromItem, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        topRow.Add(self.itemTimeType, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)

        dateStuff = wx.GridBagSizer(0, 0)
        dateStuff.Add(self.cal, (0, 0), (3, 1), border=8, flag=wx.RIGHT)
        dateStuff.Add(self.staticText2, (0, 1), border=3,
                      flag=wx.ALIGN_BOTTOM | wx.BOTTOM)
        dateStuff.Add(self.date_format, (1, 1), (1, 2), border=3, flag=wx.ALIGN_TOP | wx.RIGHT)
        dateStuff.Add(self.staticText4, (2, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        dateStuff.Add(self.dateSeperator, (2, 2), border=5,
                      flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT)

        dateBox = wx.StaticBoxSizer(self.staticBox1, wx.HORIZONTAL)
        dateBox.Add(dateStuff, 0, wx.LEFT | wx.TOP, 3)

        timeStuff = wx.GridBagSizer(0, 0)
        timeStuff.Add(self.time, (0, 0), border=5, flag=wx.LEFT | wx.ALIGN_CENTER)
        timeStuff.Add(self.spin1, (0, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        timeStuff.Add(self.setTimeNow, (1, 0), (1, 2), border=5,
                      flag=wx.TOP | wx.BOTTOM | wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        timeStuff.Add(self.staticText1, (2, 0), border=8,
                      flag=wx.LEFT | wx.ALIGN_BOTTOM)
        timeStuff.Add(self.time_format, (3, 0), (1, 2), border=10, flag=wx.LEFT)
        timeStuff.Add(self.staticText3, (5, 0), border=10,
                      flag=wx.LEFT | wx.ALIGN_CENTER)
        timeStuff.Add(self.timeSeperator, (5, 1), )

        timeBox = self.timeBox = wx.StaticBoxSizer(self.staticBox2,
                                                   wx.HORIZONTAL)
        timeBox.Add(timeStuff, 0, wx.BOTTOM | wx.TOP, 3)

        midSection = wx.BoxSizer(wx.HORIZONTAL)
        midSection.Add(dateBox, 0, wx.LEFT, 8)
        midSection.Add(timeBox, 0, wx.LEFT, 24)

        bottomRow = self.bottomRow = wx.BoxSizer(wx.HORIZONTAL)
        bottomRow.Add(self.staticText5, 0, wx.LEFT | wx.ALIGN_CENTER, 15)
        bottomRow.Add(self.dateTestDisplay, 1, wx.LEFT | wx.ALIGN_CENTER, 5)
        bottomRow.Add(self.staticText6, 0, wx.RIGHT | wx.ALIGN_CENTER, 5)
        bottomRow.Add(self.timeTestDisplay, 1, wx.RIGHT | wx.ALIGN_CENTER, 15)

        mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topRow, 0, wx.TOP | wx.EXPAND, 7)
        mainSizer.Add(midSection, 0, wx.LEFT | wx.TOP, 7)
        mainSizer.Add(bottomRow, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)

        self.SetSizerAndFit(mainSizer)

    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_PANEL, name=u'dateTimePanel',
                          parent=prnt, style=wx.TAB_TRAVERSAL)

        fontSize = app.fontParams['size']

        self.staticBox1 = wx.StaticBox(id=wxID_PANELSTATICBOX1,
                                       label=_(u"Date Settings:"), name=u'staticBox1', parent=self,
                                       style=0)

        self.staticBox2 = wx.StaticBox(id=wxID_PANELSTATICBOX2,
                                       label=_(u"Time Settings:"), name=u'staticBox2', parent=self,
                                       style=0)

        self.cal = wx.calendar.CalendarCtrl(date=wx.DateTime.Now(),
                                            id=wxID_PANELCAL, name=u'cal', parent=self,
                                            style=wx.calendar.CAL_SHOW_SURROUNDING_WEEKS | wx.calendar.CAL_MONDAY_FIRST | wx.calendar.CAL_SHOW_HOLIDAYS)
        self.cal.Bind(wx.calendar.EVT_CALENDAR_SEL_CHANGED, self._test_date,
                      id=wxID_PANELCAL)

        self.date_format = wx.ComboBox(choices=[_(u"MM-DD-YYYY"),
                                       _(u"MM-DD-YY"), _(u"DD-MM-YYYY"), _(u"DD-MM-YY"),
                                       _(u"YYYY-MM-DD"), _(u"Month DD, YYYY"), _(u"Day, Month DD, YYYY"),
                                       _(u"YY"), _(u"YYYY")], id=wxID_PANELDATE_FORMAT,
                                       name=u'date_format', parent=self, style=0, value='')
        self.date_format.SetSelection(0)
        self.date_format.SetToolTipString(_(u"Use menu or enter text"))
        self.date_format.Bind(wx.EVT_TEXT, self._test_date,
                              id=wxID_PANELDATE_FORMAT)

        self.time_format = wx.ComboBox(choices=[_(u"HH'MM"), _(u"24HH'MM"),
                                       _(u"HH'MM'SS"), _(u"24HH'MM'SS"), _(u"HHhMMm"), _(u"24HHhMMm"),
                                       _(u"HHhMMmSSs"), _(u"24HHhMMmSSs"), ], id=wxID_PANELTIME_FORMAT,
                                       name=u'time_format', parent=self, style=0)
        self.time_format.SetSelection(2)
        self.time_format.SetToolTipString(_(u"Use menu or enter text"))
        self.time_format.Bind(wx.EVT_TEXT, self._test_time,
                              id=wxID_PANELTIME_FORMAT)

        self.dateTestDisplay = wx.StaticText(id=wxID_PANELDATETESTDISPLAY,
                                             name=u'dateTestDisplay', parent=self, label='')

        self.staticText1 = wx.StaticText(id=wxID_PANELSTATICTEXT1,
                                         label=_(u"Formatting:"), name=u'staticText1', parent=self,
                                         style=0)

        self.staticText2 = wx.StaticText(id=wxID_PANELSTATICTEXT2,
                                         label=_(u"Formatting:"), name=u'staticText2', parent=self,
                                         style=0)

        self.timeTestDisplay = wx.StaticText(id=wxID_PANELTIMETESTDISPLAY,
                                             name=u'timeTestDisplay', parent=self, style=0, label='')

        self.staticText3 = wx.StaticText(id=wxID_PANELSTATICTEXT3,
                                         label=_(u"Separator:"), name=u'staticText3', parent=self,
                                         style=0)

        self.dateSeperator = wx.TextCtrl(id=wxID_PANELDATESEPERATOR,
                                         name=u'dateSeperator', parent=self,
                                         size=wx.Size(24, -1), style=0, value='-')
        self.dateSeperator.SetMaxLength(1)
        self.dateSeperator.Bind(wx.EVT_TEXT, self._test_date,
                                id=wxID_PANELDATESEPERATOR)

        self.staticText4 = wx.StaticText(id=wxID_PANELSTATICTEXT4,
                                         label=_(u"Separator:"), name=u'staticText4', parent=self,
                                         style=0)

        self.timeSeperator = wx.TextCtrl(id=wxID_PANELTIMESEPERATOR,
                                         name=u'timeSeperator', parent=self,
                                         size=wx.Size(24, -1), style=0, value="'")
        self.timeSeperator.SetMaxLength(1)
        self.timeSeperator.Bind(wx.EVT_TEXT, self._test_time,
                                id=wxID_PANELTIMESEPERATOR)

        self.spin1 = wx.SpinButton(id=wxID_PANELSPIN1, name=u'spin1',
                                   parent=self, style=wx.SP_VERTICAL)
        self.spin1.SetToolTipString(_(u"Adjust Time"))
        self.spin1.Bind(wx.EVT_SPIN, self._test_time, id=wxID_PANELSPIN1)

        self.time = wx.lib.masked.timectrl.TimeCtrl(display_seconds=True,
                                                    fmt24hr=False, id=wxID_PANELTIME, name=u'time',
                                                    oob_color=wx.NamedColour(u'Yellow'), parent=self,
                                                    spinButton=self.spin1, style=wx.TE_PROCESS_TAB,
                                                    useFixedWidthFont=True, value=wx.DateTime.Now())

        self.setTimeNow = wx.Button(id=wxID_PANELSETTIMENOW,
                                    label=_(u"Set to now"), name=u'setTimeNow', parent=self,
                                    style=0)
        self.setTimeNow.Bind(wx.EVT_BUTTON, self._on_settimenow_button,
                             id=wxID_PANELSETTIMENOW)

        self.staticText5 = wx.StaticText(id=wxID_PANELSTATICTEXT5,
                                         label=_(u"Date Preview:"), name=u'staticText5', parent=self,
                                         style=0)
        self.staticText5.SetFont(wx.Font(fontSize + 1, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.staticText6 = wx.StaticText(id=wxID_PANELSTATICTEXT6,
                                         label=_(u"Time Preview:"), name=u'staticText6', parent=self,
                                         style=0)
        self.staticText6.SetFont(wx.Font(fontSize + 1, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.getFromItem = wx.CheckBox(id=wxID_PANELGETFROMITEM,
                                       label=_(u"Get date && time from item, using:"), name=u'getFromItem',
                                       parent=self, style=0)
        self.getFromItem.SetValue(False)
        self.getFromItem.Bind(wx.EVT_CHECKBOX, self.get_from_item_checkbox,
                              id=wxID_PANELGETFROMITEM)

        self.itemTimeType = wx.Choice(choices=[self.ctime,
                                      _(u"last modification"), _(u"last access"),
                                      _(u"Exif tag - picture taken"),
                                      _(u"Exif tag - image modified")],
                                      id=wxID_PANELITEMTIMETYPE, name=u'itemTimeType',
                                      parent=self, style=0)
        self.itemTimeType.SetSelection(0)
        self.itemTimeType.Enable(False)
        self.itemTimeType.Bind(wx.EVT_CHOICE, main.show_preview,
                               id=wxID_PANELITEMTIMETYPE)

    def __init__(self, parent, main_window):
        global main
        main = main_window

        if sys.platform == u'win32':
            self.ctime = _(u"creation")
        else:
            self.ctime = _(u"metadata change")

        self.__init_ctrls(parent)
        self.__init_sizer()
        self._test_date(False)
        self._test_time(False)


    def get_from_item_checkbox(self, event):
        """Enable or disable based on whether to get from item or not."""
        enabled = (self.itemTimeType, )
        disabled = (self.cal, self.spin1, self.time, self.setTimeNow)
        if self.getFromItem.GetValue():
            for widget in enabled:
                widget.Enable(True)
            for widget in disabled:
                widget.Enable(False)
        else:
            for widget in enabled:
                widget.Enable(False)
            for widget in disabled:
                widget.Enable(True)
        self._test_time(event)
        self._test_date(event)

    def get_datetime(self, event):
        """
        get date/time, format according to user input,
        and return values. Called from 'main' module as well
        as from within this class.
        """
        self.dateTime = [False, False, False] # 0=get from?, 1=date, 2=time

        # get date/time from item or set by user
        if self.getFromItem.GetValue():
            self.dateTime[0] = True

        #-------- DATE --------#
        #translate from human readable:
        sep = self.dateSeperator.GetValue()
        date_lookup = {
            _(u"MM-DD-YYYY"): u'%m' + sep + u'%d' + sep + u'%Y',
            _(u"MM-DD-YY"): u'%m' + sep + u'%d' + sep + u'%y',
            _(u"DD-MM-YYYY"): u'%d' + sep + u'%m' + sep + u'%Y',
            _(u"DD-MM-YY"): u'%d' + sep + u'%m' + sep + u'%y',
            _(u"YYYY-MM-DD"): u'%Y' + sep + u'%m' + sep + u'%d',
            _(u"Month DD, YYYY"): u'%B %d, %Y',
            _(u"Day, Month DD, YYYY"): u'%A, %B %d, %Y',
            _(u"YY"): u'%y',
            _(u"YYYY"): u'%Y',
            }
        if event and event.GetId() == wxID_PANELDATE_FORMAT:
            date_format = event.GetString()
        else:
            date_format = self.date_format.GetValue()

        # get the format
        try:
            date_form = date_lookup[date_format]
        except KeyError:
            date_form = date_format

        # get date from item or set by user
        if self.dateTime[0]:
            self.dateTime[1] = date_form
        elif date_form:
            date = self.cal.GetDate().Format(date_form)
            self.dateTime[1] = date


        #-------- TIME --------#
        #translate from human readable:
        sep = self.timeSeperator.GetValue()
        time_lookup = {
            _(u"HH'MM"): u'%I' + sep + u'%M %p',
            _(u"24HH'MM"): u'%H' + sep + u'%M',
            _(u"HH'MM'SS"): u'%I' + sep + u'%M' + sep + u'%S %p',
            _(u"24HH'MM'SS"): u'%H' + sep + u'%M' + sep + u'%S',
            _(u"HHhMMm"): u'%Ih%Mm %p',
            _(u"24HHhMMm"): u'%Hh%Mm',
            _(u"HHhMMmSSs"): u'%Ih%Mm%Ss %p',
            _(u"24HHhMMmSSs"): u'%Hh%Mm%Ss',
            }

        if event and event.GetId() == wxID_PANELTIME_FORMAT:
            time_format = event.GetString()
        else:
            time_format = self.time_format.GetValue()

        # get the format
        try:
            time_form = time_lookup[time_format]
        except KeyError:
            time_form = time_format

        # get time from item or set by user
        if self.dateTime[0]:
            self.dateTime[2] = time_form
        else:
            time = self.time.GetWxDateTime()
            try:
                time = time.Format(time_form)
            except:
                time = ''
                pass
            self.dateTime[2] = time
    #------------------------------------------------#


    def _test_date(self, event):
        """Display date according to current settings."""
        self.get_datetime(event)
        if self.dateTime[1]:
            self.dateTestDisplay.SetLabel(self.dateTime[1])
            main.show_preview(event)

    def _test_time(self, event):
        """Displays time according to current settings."""
        self.get_datetime(event)
        if self.dateTime[2]:
            self.timeTestDisplay.SetLabel(self.dateTime[2])
            main.show_preview(event)

    def _on_settimenow_button(self, event):
        self.time.SetValue(wx.DateTime.Now())
        self._test_time(event)
