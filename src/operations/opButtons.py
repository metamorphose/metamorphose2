# -*- coding: utf-8 -*-

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

import opParser
import utils
import wx

[wxID_PANEL, wxID_PANELID3, wxID_PANELID3SELECT, wxID_PANELINSDATE,
    wxID_PANELINS_NUM, wxID_PANELINSTIME, wxID_PANELSTATICTEXT1,
    wxID_PANELEXIF, wxID_PANELEXIFSELECT, wxID_PANELFOLDER,
    wxID_PANELFOLDERDEPTH
] = [wx.NewId() for __init_ctrls in range(11)]

class Panel(wx.Panel):
    """"
    Helper panel to some of the operations panels.
    It allows the usage of buttons to insert sub-operations,
    and contains the associated sub-operations.
    """

    def __init_sizer(self):

        mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.staticText1, 0, wx.TOP | wx.LEFT, 5)

        buttonSizer = self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add(self.ins_num, 0, wx.LEFT | wx.ALIGN_CENTER, 4)
        buttonSizer.Add(self.insDate, 0, wx.LEFT | wx.ALIGN_CENTER, 8)
        buttonSizer.Add(self.insTime, 0, wx.LEFT | wx.ALIGN_CENTER, 8)
        buttonSizer.Add(self.id3select, 0, wx.LEFT | wx.ALIGN_CENTER, 8)
        buttonSizer.Add(self.EXIFselect, 0, wx.RIGHT | wx.LEFT | wx.ALIGN_CENTER, 8)
        buttonSizer.Add(self.folder, 0, wx.RIGHT | wx.ALIGN_CENTER, 2)
        buttonSizer.Add(self.folderDepth, 0, wx.RIGHT | wx.ALIGN_CENTER, 4)
        mainSizer.Add(buttonSizer, 0, wx.EXPAND | wx.TOP, 2)
        self.SetSizerAndFit(mainSizer)


    def __init_ctrls(self, prnt, Name):
        wx.Panel.__init__(self, id=wxID_PANEL, name=Name, parent=prnt,
                          style=wx.TAB_TRAVERSAL,)

        self.staticText1 = wx.StaticText(id=wxID_PANELSTATICTEXT1,
                                         label=_(u"Insert a special operation:"), name='staticText1',
                                         parent=self, style=0)

        self.ins_num = wx.Button(id=wxID_PANELINS_NUM,
                                 label=_(u"numbering"), name=u'ins_num', parent=self, style=wx.BU_EXACTFIT)
        self.ins_num.SetToolTipString(_(u"Insert enumerating sequence. Use the 'Numbering settings'\npanel to change settings"))
        self.ins_num.Bind(wx.EVT_BUTTON, self._on_number_button,
                          id=wxID_PANELINS_NUM)

        self.insDate = wx.Button(id=wxID_PANELINSDATE, label=_(u"date"),
                                 name=u'insDate', parent=self, style=wx.BU_EXACTFIT)
        self.insDate.SetToolTipString(_(u"Insert date. Use the 'Date / Time settings' panel to\nchange settings"))
        self.insDate.Bind(wx.EVT_BUTTON, self._on_date_button,
                          id=wxID_PANELINSDATE)

        self.insTime = wx.Button(id=wxID_PANELINSTIME, label=_(u"time"),
                                 name=u'insTime', parent=self, style=wx.BU_EXACTFIT)
        self.insTime.SetToolTipString(_(u"Insert time. Use the 'Date / Time settings' panel to\nchange settings"))
        self.insTime.Bind(wx.EVT_BUTTON, self._on_time_button,
                          id=wxID_PANELINSTIME)

        self.id3select = wx.Choice(choices=[
                                   _(u"audio info"),
                                   _('artist'),
                                   _('album'),
                                   _('disc number'),
                                   _('track number'),
                                   _('title'),
                                   _('genre'),
                                   _('performer'),
                                   _('date'),
                                   _('author'),
                                   _('composer'),
                                   _('conductor'),
                                   _('lyricist'),
                                   _('comment'),
                                   #_('version'),
                                   #_('language'),
                                   #_('encoded by'),
                                   ],
                                   id=wxID_PANELID3SELECT, name=u'id3select', parent=self)
        self.id3select.SetSelection(0)
        self.id3select.SetToolTipString(_(u"Insert id3 tag information from mp3 file"))
        self.id3select.Bind(wx.EVT_CHOICE, self._on_id3, id=wxID_PANELID3SELECT)

        self.EXIFselect = wx.Choice(choices=[
                                    _(u"image info"),
                                    #_(u"date taken"),
                                    #_(u"date modified"),
                                    _(u"width"),
                                    _(u"height"),
                                    _(u"width") + u":x:" + _(u"height"),
                                    _(u"X-resolution"),
                                    _(u"Y-resolution"),
                                    _(u"X-res") + u":x:" + _(u"Y-res"),
                                    _(u"orientation"),
                                    _(u"exposure"),
                                    _(u"F-stop"),
                                    _(u"flash"),
                                    _(u"focal-length"),
                                    _(u"ISO"),
                                    _(u"shutter-speed"),
                                    _(u"copyright"),
                                    _(u"make"),
                                    _(u"model"),
                                    _(u"unit"),
                                    _(u"software")],
                                    id=wxID_PANELEXIFSELECT, name=u'EXIFselect', parent=self,
                                    size=wx.Size(128, -1))
        self.EXIFselect.SetSelection(0)
        self.EXIFselect.SetToolTipString(_(u"Insert Exif tag information from tiff or jpeg file.\nUse the date button to insert Exif date"))
        self.EXIFselect.Bind(wx.EVT_CHOICE, self._on_exif, id=wxID_PANELEXIFSELECT)

        self.folder = wx.Button(id=wxID_PANELFOLDER, label=_(u"folder:"),
                                name=u'folder', parent=self, style=wx.BU_EXACTFIT)
        self.folder.SetToolTipString(_(u"Insert parent folder name"))
        self.folder.Bind(wx.EVT_BUTTON, self._on_folder_button, id=wxID_PANELFOLDER)

        self.folderDepth = wx.SpinCtrl(id=wxID_PANELFOLDERDEPTH,
                                       initial=1, max=999, min=1, name=u'folderDepth',
                                       parent=self, pos=wx.Point(200, 104), size=wx.Size(50, -1),
                                       value='1', style=wx.SP_ARROW_KEYS)
        self.folderDepth.SetValue(1)
        self.folderDepth.SetToolTipString(_(u"How far back to get folder"))


    def __init__(self, prnt, main_window, name=u'opButtonsPanel'):
        global main
        main = main_window
        self.parent = prnt
        self.parser = opParser.Parser(main)
        self.__init_ctrls(prnt, name)
        # adjust button sizes
        utils.adjust_exact_buttons(self)
        self.__init_sizer()

#### BUTTONS ##################################################################
    def _insert_text(self, txt):
        if self.parent.activatedField:
            txt = u":" + txt + u":"
            iPoint = self.parent.activatedField.GetInsertionPoint()
            self.parent.activatedField.WriteText(txt)
            self.parent.activatedField.SetFocus()
            self.parent.activatedField.SetInsertionPoint(iPoint + len(txt))

    def _on_number_button(self, event):
        self._insert_text(_(u"numb"))

    def _on_date_button(self, event):
        self._insert_text(_(u"date"))

    def _on_time_button(self, event):
        self._insert_text(_(u"time"))

    def _on_id3(self, event):
        if self.id3select.GetSelection() != 0:
            self._insert_text(self.id3select.GetStringSelection())
            self.id3select.SetSelection(0)

    def _on_exif(self, event):
        if self.EXIFselect.GetSelection() != 0:
            self._insert_text(self.EXIFselect.GetStringSelection())
            self.EXIFselect.SetSelection(0)

    def _on_folder_button(self, event):
        self._insert_text(_(u"folder%s") % self.folderDepth.GetValue())


    def parse_input(self, text, file, operation):
        """
        Parse the active fields for sub operations and return
        the corresponding result in place.
        """
        return self.parser.parse_input(text, file, operation)
