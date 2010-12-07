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

"""
Panel to hold change case widgets and operations.

Uses search panel.
"""

import wx
from operation import Operation
import search
import utils
import sre_constants
import accentStrip

[wxID_PANEL, wxID_PANELOTHER_OPERATION_VALUE, wxID_PANELSTATICTEXT1,
 wxID_PANELOTHERMOD, wxID_PANELCASEMOD, wxID_PANELCASE_OPERATION_VALUE,
 wxID_PANELENCODINGGROUP, wxID_PANELFIXENCODE, wxID_PANELENCODINGSELECT
] = [wx.NewId() for __init_ctrls in range(9)]

# taken from urllib standard python library
_hextochr = dict(('%02x' % i, chr(i)) for i in range(256))
_hextochr.update(('%02X' % i, chr(i)) for i in range(256))

class OpPanel(Operation):
    """
    Operation panel for modification.
    """

    def __init_sizer(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.search,0,wx.EXPAND|wx.TOP,10)
        self.encodeSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.encodeSizer.Add(self.encodingGroup,0)

        bottomSizer = wx.FlexGridSizer(cols=2,hgap=5,vgap=15)
        bottomSizer.Add(self.caseMod,0,wx.ALIGN_CENTER_VERTICAL)
        bottomSizer.Add(self.case_operation_value,0)
        bottomSizer.Add(self.otherMod,0,wx.ALIGN_CENTER_VERTICAL)
        bottomSizer.Add(self.other_operation_value,0)
        bottomSizer.Add(self._fix_encode,0,wx.ALIGN_CENTER_VERTICAL)
        bottomSizer.Add(self.encodeSizer)

        mainSizer.Add(bottomSizer,0,wx.TOP,20)

        self.SetSizerAndFit(mainSizer)

    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=-1, name=u'modificationPanel', parent=prnt,
              style=wx.TAB_TRAVERSAL)

        self.case_operation_value = wx.Choice(choices=[_(u"UPPERCASE"),
              _(u"lowercase"), _(u"SWAP case"),
              _(u"Capitalize first"), _(u"Title Style"), _(u"DoRkIfY")],
              id=wxID_PANELCASE_OPERATION_VALUE, name=u'case_operation_value',
              parent=self, size=wx.Size(235, -1), style=0)
        self.case_operation_value.SetSelection(0)

        self.caseMod = wx.RadioButton(id=wxID_PANELCASEMOD, label=_(u"Change Case:"),
              name=u'caseMod', parent=self, style=wx.RB_GROUP)
        self.caseMod.SetValue(True)
        self.caseMod.Bind(wx.EVT_RADIOBUTTON, self.create_operation,
              id=wxID_PANELCASEMOD)

        self.other_operation_value = wx.Choice(choices=[_(u"Remove Accents"),
              _("Convert '%xx' escapes to text"),_(u"Convert text to 1337")],
              id=wxID_PANELOTHER_OPERATION_VALUE, name=u'other_operation_value',
              parent=self, size=wx.Size(235, -1), style=0)
        self.other_operation_value.SetSelection(0)

        self.otherMod = wx.RadioButton(id=wxID_PANELOTHERMOD, label=_(u"Change Characters:"),
              name=u'otherMod', parent=self, style=0)
        self.otherMod.SetValue(False)
        self.otherMod.Bind(wx.EVT_RADIOBUTTON, self.create_operation,
              id=wxID_PANELOTHERMOD)

        self._fix_encode = wx.RadioButton(id=wxID_PANELFIXENCODE, label=_(u"Convert from Encoding:"),
              name=u'_fix_encode', parent=self, style=0)
        self._fix_encode.SetValue(False)
        self._fix_encode.Bind(wx.EVT_RADIOBUTTON, self.create_operation,
              id=wxID_PANELFIXENCODE)

        self.encodingGroup = wx.Choice(choices=[_(u'All Languages / Unicode'),
              _(u'Western Europe'),
              _(u'Central & Eastern Europe'), _(u'Esperanto, Maltese'),
              _(u'Nordic Languages'), _(u'Celtic Languages'),
              _(u'Baltic Languages'), _(u'Cyrillic Languages'), _(u'Greek'),
              _(u'Turkish'), _(u'Hebrew'), _(u'Arabic'), _(u'Urdu'), _(u'Thai'),
              _(u'Vietnamese'), _(u'Traditional Chinese'),
              _(u'Simplified Chinese'), _(u'Unified Chinese'), _(u'Korean'),
              _(u'Japanese'), ], id=wxID_PANELENCODINGGROUP,
              name=u'encodingGroup', parent=self, style=0)
        self.encodingGroup.SetSelection(0)
        self.encodingGroup.Bind(wx.EVT_CHOICE, self._encoding_options,
              id=wxID_PANELENCODINGGROUP)


    def __init__(self, parent, main_panel, params={}):
        Operation.__init__(self, params)
        global main
        main = main_panel
        self.__init_ctrls(parent)

        # place these here for boa compatibility
        self.case_operation_value.Bind(wx.EVT_CHOICE, self.create_operation,
              id=wxID_PANELCASE_OPERATION_VALUE)
        self.other_operation_value.Bind(wx.EVT_CHOICE, self.create_operation,
              id=wxID_PANELOTHER_OPERATION_VALUE)
        self.search = search.Panel(self, main, _(u"Search for what to modify, by:"))

        self.__init_sizer()
        self.on_config_load()

    def on_config_load(self):
        """Update GUI elements, settings after config load."""
        self._encoding_options(False)
        self.create_operation(False)
        self.search.on_load(0)

    def _make_encoding_select(self, choicesList):
        self.encodingSelect = wx.Choice(choices=choicesList,
              id=wxID_PANELENCODINGSELECT, name=u'encodingSelect', parent=self)
        self.encodingSelect.Bind(wx.EVT_CHOICE, self.create_operation,
              id=wxID_PANELENCODINGSELECT)
        self.encodeSizer.Add(self.encodingSelect, 0, border=5, flag=wx.LEFT)
        self.Layout()

    def _encoding_options(self, event):
        Value = self.encodingGroup.GetStringSelection()
        try:
            self.encodingSelect.Destroy()
        except AttributeError:
            pass
        choicesList = utils.get_encoding_choices(Value)
        self._make_encoding_select(choicesList)
        self.encodingSelect.SetSelection(0)
        self.create_operation(event)


    def unquote(self, s):
        """
        unquote('abc%20def') -> 'abc def'.

        Taken from urllib standard python library.
        """
        res = s.split('%')
        for i in xrange(1, len(res)):
            item = res[i]
            try:
                res[i] = _hextochr[item[:2]] + item[2:]
            except KeyError:
                res[i] = '%' + item
            except UnicodeDecodeError:
                res[i] = unichr(int(item[:2], 16)) + item[2:]
        return "".join(res)

    def create_operation(self, event):
        if not event:
            pass
        # no need to have user select RB
        elif event.GetId() == wxID_PANELOTHER_OPERATION_VALUE:
            self.otherMod.SetValue(True)
        elif event.GetId() == wxID_PANELCASE_OPERATION_VALUE:
            self.caseMod.SetValue(True)
        elif event.GetId() == wxID_PANELENCODINGGROUP or \
          event.GetId() == wxID_PANELENCODINGSELECT:
            self._fix_encode.SetValue(True)
        searchValues = self.search.searchValues

        if searchValues[0] == u"reg-exp" and searchValues[2]:
            isRegExp = True
        else:
            isRegExp = False

        # case modifications
        def uppercase(match):
            if isRegExp:
                match = match.group()
            return match.upper()
        def lowercase(match):
            if isRegExp:
                match = match.group()
            return match.lower()
        def capitalize(match):
            if isRegExp:
                match = match.group()
            return match.capitalize()
        def title(match):
            if isRegExp:
                match = match.group()
            return match.title()
        def swapcase(match):
            if isRegExp:
                match = match.group()
            return match.swapcase()
        def dorkify(match):
            if isRegExp:
                match = match.group()
            i = 0
            newString = u''
            for char in match:
                i += 1
                if i == 2:
                    newString += char.lower()
                    i = 0
                else:
                    newString += char.upper()
            return newString

        # other modifications
        def _strip_accents(match):
            if isRegExp:
                match = match.group()
            return accentStrip.full_convert(match)
        def _url_decode(match):
            if isRegExp:
                match = match.group()
            return self.unquote(match)
        def _to_l337(match):
            if isRegExp:
                match = match.group()
            lookup = {
                      u"A" : u"4",
                      u"a" : u"@",
                      u"B" : u"8",
                      u"C" : u"(",
                      u"D" : u"[}",
                      u"E" : u"&",
                      u"e" : u"3",
                      u"G" : u"9",
                      u"g" : u"9",
                      u"H" : u"}-{",
                      u"L" : u"1",
                      u"i" : u"!",
                      u"O" : u"()",
                      u"o" : u"0",
                      u"Q" : u"(),",
                      u"q" : u"0,",
                      u"S" : u"5",
                      u"s" : u"5",
                      u"T" : u"7",
                      u"t" : u"+",
                      u"Z" : u"2",
                     }
            for char in lookup.keys():
                match = match.replace(char, lookup[char])
            return match

        def _fix_encode(match):
            if isRegExp:
                match = match.group()
            enc = self.encodingSelect.GetStringSelection()
            match = match.encode(enc,'backslashreplace')
            match = unicode(match, 'utf_8', 'replace')
            return match

        # set possible modifications and selected operation:
        if self.caseMod.GetValue():
            self.comds = (uppercase,lowercase,swapcase,capitalize,title,dorkify)
            self.op = self.case_operation_value.GetSelection()
        elif self.otherMod.GetValue():
            self.comds = (_strip_accents,_url_decode,_to_l337,)
            self.op = self.other_operation_value.GetSelection()
        elif self._fix_encode.GetValue():
            self.comds = (_fix_encode,)
            self.op = 0
        main.show_preview(event)


    def rename_item(self, path, name, ext, original):
        newName = newName = self.join_ext(name,ext)
        if not newName:
            return path,name,ext

        # basic settings
        search = self.search
        searchValues = search.searchValues
        if searchValues[0] == u"reg-exp" and searchValues[1]:
            isRegExp = True
        else:
            isRegExp = False

        # do the modifications based on selected operations

        # regular expression
        if isRegExp:
            try:
                newName = searchValues[2].sub(self.comds[self.op], newName)
            except (sre_constants.error,AttributeError) as err:
                main.set_status_msg(_(u"Regular-Expression: %s")%err,u'warn')
                # so we know not to change status text after RE error msg:
                main.REmsg = True
                pass
            # show RE error message from search, if any
            if search.REmsg:
                main.set_status_msg(search.REmsg,u'warn')
                main.REmsg = True
        # text
        elif searchValues[0] == u"text" and searchValues[2]:
            find = searchValues[2]
            #case insensitive
            if not searchValues[1]:
                found = search.case_insensitive(newName)
                for match in found:
                    newName = newName.replace(match, self.comds[self.op](find))
            #case sensitive:
            else:
                newName = newName.replace(find, self.comds[self.op](find))
        # between
        elif searchValues[0] == u"between":
            positions = search.get_between_to_from(newName)
            if positions:
                frm = positions[0]
                to = positions[1]
                newName = newName[:frm] + self.comds[self.op](newName[frm:to]) + newName[to:]
        # positioning:
        elif searchValues[0] == u"position":
            ss = search.repl_from.GetValue()
            sl = search.repl_len.GetValue()
            frm,to,tail = search.get_start_end_pos(ss,sl,newName)
            # apply positioning
            newName = newName[:frm] + self.comds[self.op](newName[frm:to]) + tail
        #nothing set, change entire name:
        else:
            newName = self.comds[self.op](newName)

        name,ext = self.split_ext(newName,name,ext)
        return path,name,ext

