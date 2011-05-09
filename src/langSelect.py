# -*- coding: utf-8 -*-

# Dialog to select interface language

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

import utils
import wx

def create(parent, Title, event):
    return LangSelect(parent, Title, event)

languages = (
			 #('ar', u'العربية', 'sa'),
			 #('ca', u'Català', 'es_ct'),
			 #('da', u'Dansk', 'dk'),
			 #('de', u'Deutsch', 'de'),
			 #('el', u'Ελληνικά', 'gr'),
			 ('en_US', u'US English', 'us'),
			 ('es', u'Español', 'es'),
			 ('fr', u'Français', 'fr'),
			 #('he', u'עברית', 'il'),
			 #('hi', u'हिन्दी', 'in'),
			 #('hu', u'Magyar', 'hu'),
			 #('it', u'Italiano', 'it'),
			 #('ja', u'日本語', 'jp'),
			 #('ko', u'한국어', 'kr'),
			 #('nl', u'Nederlands', 'nl'),
			 #('pl', u'Polski', 'pl'),
			 #('pt_BR', u'Português do Brasil', 'br'),
			 #('tr', u'Türkçe', 'tr'),
			 #('ru', u'Русский', 'ru'),
			 #('sk', u'Slovenčina', 'si'),
			 #('sv', u'Svenska', 'se'),
			 #('zh_CN', u'中文', 'cn'),
			 )

class LangSelect(wx.Dialog):
    def __init_sizer(self):
        optionsSizer = wx.FlexGridSizer(rows=3, cols=2, hgap=2, vgap=10)

        # add languages to sizer
        for lang_info in languages:
            lang_flag = getattr(self, '%s_flag' % lang_info[0])
            lang_select = getattr(self, lang_info[0])
            optionsSizer.Add(lang_flag, 0, wx.ALIGN_CENTRE | wx.RIGHT, 5)
            optionsSizer.Add(lang_select)

        buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsSizer.Add(self.ok, 0, wx.RIGHT | wx.LEFT, 5)
        buttonsSizer.Add(self.cancel, 0, wx.RIGHT, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(optionsSizer, 0, wx.ALIGN_CENTRE | wx.BOTTOM | wx.TOP, 10)
        sizer.Add(buttonsSizer, 0, wx.BOTTOM | wx.TOP, 5)

        self.SetSizerAndFit(sizer)


    def __init_ctrls(self, prnt, Title):
        wx.Dialog.__init__(self, id=-1, name=u'langSelect',
						   parent=prnt, size=wx.Size(281, 292),
						   style=wx.DEFAULT_DIALOG_STYLE, title=Title)
        self.SetIcon(wx.Icon(utils.icon_path(u'language.png'), wx.BITMAP_TYPE_PNG))

        def getBitmap(lang):
            return wx.Bitmap(utils.icon_path(u'flags/%s.png' % lang), wx.BITMAP_TYPE_PNG)

        # add languages selection to interface
        for lang_info in languages:
            lang = lang_info[0]
            setattr(self, lang, wx.RadioButton(id=-1, label=lang_info[1],
					name=lang, parent=self, style=0))
            getattr(self, lang).SetToolTipString(u"%s (%s)" % (lang_info[1], lang))
            setattr(self, '%s_flag' % lang, wx.StaticBitmap(parent=self, id=-1,
					bitmap=getBitmap(lang_info[2])))

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
