# -*- coding: utf-8 -*-

# Dialog to select interface language

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
import utils

def create(parent, Title, event):
    return LangSelect(parent, Title, event)

[wxID_LANGSELECT,
] = [wx.NewId() for __init_ctrls in range(1)]

languages = (
    ('en_US', u'English', u'American English (en_US)'),
    ('es', u'Español', u'Español (es)'),
    ('fr', u'Français', u'Français (fr)'),
)


class LangSelect(wx.Dialog):
    def __init_sizer(self):
        optionsSizer = wx.FlexGridSizer(rows=3, cols=2, hgap=2, vgap=10)

        # add languages to sizer
        for lang_info in languages:
            lang_flag = getattr(self, '%s_flag'%lang_info[0])
            lang_select = getattr(self, lang_info[0])
            optionsSizer.Add(lang_flag,0, wx.ALIGN_CENTRE|wx.RIGHT, 5)
            optionsSizer.Add(lang_select)

        buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsSizer.Add(self.ok,0,wx.RIGHT|wx.LEFT,5)
        buttonsSizer.Add(self.cancel,0,wx.RIGHT,5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(optionsSizer,0,wx.ALIGN_CENTRE|wx.BOTTOM|wx.TOP,10)
        sizer.Add(buttonsSizer,0,wx.BOTTOM|wx.TOP,5)

        self.SetSizerAndFit(sizer)


    def __init_ctrls(self, prnt, Title):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_LANGSELECT, name=u'langSelect',
              parent=prnt, size=wx.Size(281, 292),
              style=wx.DEFAULT_DIALOG_STYLE, title=Title)
        self.SetIcon(wx.Icon(utils.icon_path(u'language.png'), wx.BITMAP_TYPE_PNG))

        def getBitmap(lang):
            fLang = lang.replace('_*', '')
            return wx.Bitmap(utils.icon_path(u'flags/%s.png'%fLang), wx.BITMAP_TYPE_PNG)

        # add languages selection to interface
        for lang_info in languages:
            lang = lang_info[0]
            setattr(self, lang, wx.RadioButton(id=-1, label=lang_info[1],
                                name=lang, parent=self, style=0))
            getattr(self, lang).SetToolTipString(lang_info[2])
            setattr(self, '%s_flag'%lang, wx.StaticBitmap(parent=self, id=-1,
                                          bitmap=getBitmap(lang)))

        self.ok = wx.Button(id=wx.ID_OK, name=u'ok',
              parent=self, pos=wx.Point(20, 300), style=0)

        self.cancel = wx.Button(id=wx.ID_CANCEL, name=u'cancel',
              parent=self, pos=wx.Point(120, 300), style=0)

    def __init__(self, parent, Title, event):
        self.__init_ctrls(parent, Title)
        self.__init_sizer()
        if event:
            self.FindWindowByName(event).SetValue(True)
        else:
            self.en_US.SetValue(True)
            self.cancel.Show(False)

    def GetLanguage(self):
        notLangs = ('staticBitmap', 'ok', 'cancel')
        for child in self.GetChildren():
            name = child.GetName()
            if name not in notLangs:
                if child.GetValue():
                    return name
