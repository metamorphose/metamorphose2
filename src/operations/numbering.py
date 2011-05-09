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

import utils
import wx

[wxID_PANEL, wxID_PANELALPHA, wxID_PANELALPHA_PAD, wxID_PANELALPHA_UC,
	wxID_PANELASC, wxID_PANELCOUNT, wxID_PANELCOUNTBYDIR, wxID_PANELDESC,
	wxID_PANELDIGIT, wxID_PANELDIGIT_AUTOPAD, wxID_PANELDIGIT_PAD,
	wxID_PANELDIGIT_SETPAD, wxID_PANELPAD_CHAR, wxID_PANELPAD_WIDTH,
	wxID_PANELREPEAT, wxID_PANELRESET, wxID_PANELRESETDIR, wxID_PANELROMAN,
	wxID_PANELROMAN_UC, wxID_PANELSTART, wxID_PANELSTARTBYITEMS,
	wxID_PANELSTATICTEXT1, wxID_PANELSTATICTEXT3, wxID_PANELSTATICTEXT5,
	wxID_PANELSTATICTEXT6, wxID_PANELSTATICTEXT7, wxID_PANELSTEP,
	wxID_PANELSTYLE, wxID_PANELSPECIAL, wxID_PANELRINCREMENTONDIFF,
] = [wx.NewId() for __init_ctrls in range(30)]

class Panel(wx.Panel):
    """
    The numbering panel that goes into an operation's notebook.
    """
    
    def __init_num1_sizer(self, parent):
        parent.AddWindow(self.digit, 0, border=0, flag=0)
        parent.AddWindow(self.digit_pad, 0, border=0, flag=0)
        parent.AddWindow(self.pad_char, 0, border=0, flag=0)

    def __init_main_sizer(self, parent):
        parent.AddSizer(self.styleSizer, 0, border=10, flag=wx.LEFT | wx.TOP)
        parent.AddSpacer(wx.Size(30, 8), border=0, flag=0)
        parent.AddSizer(self.countSizer, 0, border=10, flag=wx.TOP)

    def __init_style_sizer(self, parent):
        parent.AddSizer(self.num1Sizer, 0, border=8, flag=wx.TOP | wx.LEFT)
        parent.AddSpacer(wx.Size(8, 5), border=0, flag=0)
        parent.AddWindow(self.digit_autopad, 0, border=24, flag=wx.LEFT)
        parent.AddSpacer(wx.Size(8, 5), border=0, flag=0)
        parent.AddSizer(self.num2Sizer, 0, border=24, flag=wx.LEFT)
        parent.AddSpacer(wx.Size(8, 10), border=0, flag=wx.TOP)
        parent.AddSizer(self.alpha1Sizer, 0, border=8, flag=wx.TOP | wx.LEFT)
        parent.AddSpacer(wx.Size(8, 5), border=0, flag=0)
        parent.AddWindow(self.alphaPad, 0, border=24, flag=wx.LEFT)
        parent.AddSpacer(wx.Size(8, 10), border=0, flag=0)
        parent.AddSizer(self.romanSizer, 0, border=10, flag=wx.ALL)

    def __init_resetby_sizer(self, parent):
        parent.AddWindow(self.resetDir, 0, border=0, flag=0)
        parent.AddWindow(self.incrementOnDiff, 0, border=2, flag=wx.BOTTOM)


    def __init_num2_sizer(self, parent):
        parent.AddWindow(self.digitSetpad, 0, border=0, flag=0)
        parent.AddWindow(self.padWidth, 0, border=0, flag=0)

    def __init_alpha1_sizer(self, parent):
        parent.AddWindow(self.alpha, 0, border=0, flag=0)
        parent.AddWindow(self.alphaUc, 0, border=0, flag=0)

    def __init_count_sizer(self, parent):
        parent.AddSizer(self.countOpSizer, 0, border=8, flag=wx.ALL)

    def __init_countop_sizer(self, parent):
        parent.AddWindow(self.staticText5, 0, border=0,
						 flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddWindow(self.start, 0, border=0, flag=0)
        parent.AddWindow(self.startByItems, 0, border=0, flag=0)
        parent.AddWindow(self.staticText6, 0, border=0,
						 flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddWindow(self.asc, 0, border=0, flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddWindow(self.desc, 0, border=0, flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddWindow(self.staticText7, 0, border=0,
						 flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddWindow(self.step, 0, border=0, flag=0)
        parent.AddWindow(self.countByDir, 0, border=5, flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        parent.AddWindow(self.staticText3, 0, border=0,
						 flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddWindow(self.repeat, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.staticText1, 0, border=0,
						 flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddWindow(self.reset, 0, border=0, flag=wx.ALIGN_CENTER_VERTICAL)
        parent.AddSizer(self.resetBySizer, 0, border=5, flag=wx.RIGHT | wx.LEFT)

    def __init_roman_sizer(self, parent):
        parent.AddWindow(self.roman, 0, border=0, flag=0)
        parent.AddWindow(self.roman_uc, 0, border=0, flag=0)

    def __init_sizers(self):
        self.mainSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.styleSizer = wx.StaticBoxSizer(box=self.style, orient=wx.VERTICAL)
        self.countSizer = wx.StaticBoxSizer(box=self.count, orient=wx.VERTICAL)
        self.resetBySizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.num1Sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.num2Sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.alpha1Sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.romanSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.countOpSizer = wx.FlexGridSizer(cols=3, hgap=8, rows=0, vgap=8)

        self.__init_num1_sizer(self.num1Sizer)
        self.__init_num2_sizer(self.num2Sizer)
        self.__init_alpha1_sizer(self.alpha1Sizer)
        self.__init_roman_sizer(self.romanSizer)
        self.__init_countop_sizer(self.countOpSizer)
        self.__init_main_sizer(self.mainSizer)
        self.__init_style_sizer(self.styleSizer)
        self.__init_count_sizer(self.countSizer)
        self.__init_resetby_sizer(self.resetBySizer)

        self.SetSizer(self.mainSizer)

    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_PANEL, name=u'numberingPanel',
						  parent=prnt, style=wx.TAB_TRAVERSAL)

        self.count = wx.StaticBox(id=wxID_PANELCOUNT, label=_(u"Counter:"),
								  name=u'count', parent=self, style=0)

        self.style = wx.StaticBox(id=wxID_PANELSTYLE, label=_(u"Style:"),
								  name=u'style', parent=self, style=0)

        self.digit = wx.RadioButton(id=wxID_PANELDIGIT, label=_(u"Numerical:"),
									name=u'digit', parent=self, style=wx.RB_GROUP)
        self.digit.SetValue(True)
        self.digit.Bind(wx.EVT_RADIOBUTTON, self._check_styles,
						id=wxID_PANELDIGIT)

        self.alpha = wx.RadioButton(id=wxID_PANELALPHA,
									label=_(u"Alphabetical:"), name=u'alpha', parent=self, style=0)
        self.alpha.SetValue(False)
        self.alpha.Enable(True)
        self.alpha.SetToolTipString(_(u"Must start at positive value: (1=a, 28=ab, etc..)"))
        self.alpha.Bind(wx.EVT_RADIOBUTTON, self._check_styles)

        self.roman = wx.RadioButton(id=wxID_PANELROMAN,
									label=_(u"Roman Numeral:"), name=u'roman', parent=self, style=0)
        self.roman.SetValue(False)
        self.roman.Enable(True)
        self.roman.SetToolTipString(_(u"Count must be between 1 and 4999"))
        self.roman.Bind(wx.EVT_RADIOBUTTON, self._check_styles)

        self.digit_pad = wx.CheckBox(id=wxID_PANELDIGIT_PAD,
									 label=_(u"Pad, using:"), name=u'digit_pad', parent=self, style=0)
        self.digit_pad.SetValue(True)
        self.digit_pad.Enable(False)
        self.digit_pad.Bind(wx.EVT_CHECKBOX, self._check_styles)

        self.digit_autopad = wx.RadioButton(id=wxID_PANELDIGIT_AUTOPAD,
											label=_(u"Auto pad"), name=u'digit_autopad', parent=self,
											style=wx.RB_GROUP)
        self.digit_autopad.SetValue(True)
        self.digit_autopad.Bind(wx.EVT_RADIOBUTTON, self._check_styles)

        self.pad_char = wx.TextCtrl(id=wxID_PANELPAD_CHAR, name=u'pad_char',
									parent=self, size=wx.Size(24, -1), style=0, value='0')
        self.pad_char.SetMaxLength(1)
        self.pad_char.Enable(False)
        self.pad_char.Bind(wx.EVT_TEXT, self._check_styles)

        self.digitSetpad = wx.RadioButton(id=wxID_PANELDIGIT_SETPAD,
										  label=_(u"Fixed pad width:"), name=u'digitSetpad', parent=self,
										  style=0)
        self.digitSetpad.SetValue(False)
        self.digitSetpad.Enable(False)
        self.digitSetpad.Bind(wx.EVT_RADIOBUTTON, self._check_styles)

        self.alphaPad = wx.CheckBox(id=wxID_PANELALPHA_PAD,
									label=_(u"auto pad"), name=u'alphaPad', parent=self, style=0)
        self.alphaPad.SetValue(True)
        self.alphaPad.Enable(False)
        self.alphaPad.Bind(wx.EVT_CHECKBOX, self._check_styles)

        self.alphaUc = wx.CheckBox(id=wxID_PANELALPHA_UC,
								   label=_(u"Uppercase"), name=u'alphaUc', parent=self,
								   style=0)
        self.alphaUc.SetValue(False)
        self.alphaUc.Enable(False)
        self.alphaUc.Bind(wx.EVT_CHECKBOX, self._check_styles)

        self.padWidth = wx.SpinCtrl(id=wxID_PANELPAD_WIDTH, initial=3, max=255,
									min=1, name=u'padWidth', parent=self, size=wx.Size(60, -1),
									style=wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER, value='3')
        self.padWidth.SetValue(3)
        self.padWidth.Enable(False)
        self.padWidth.Bind(wx.EVT_TEXT_ENTER, self._on_padwidth_spinctrl)
        self.padWidth.Bind(wx.EVT_SPINCTRL, self._on_padwidth_spinctrl)

        self.roman_uc = wx.CheckBox(id=wxID_PANELROMAN_UC,
									label=_(u"Uppercase"), name=u'roman_uc', parent=self,
									style=0)
        self.roman_uc.SetValue(True)
        self.roman_uc.Enable(False)
        self.roman_uc.Bind(wx.EVT_CHECKBOX, self._check_styles)

        self.staticText5 = wx.StaticText(id=wxID_PANELSTATICTEXT5,
										 label=_(u"Start at:"), name=u'staticText5', parent=self,
										 style=0)

        self.step = wx.SpinCtrl(id=wxID_PANELSTEP, initial=1, max=10000000,
								min=1, name=u'step', parent=self, size=wx.Size(70, -1),
								style=wx.SP_ARROW_KEYS, value='1')
        self.step.SetValue(1)
        self.step.SetToolTipString(_(u"Step size"))
        self.step.Bind(wx.EVT_TEXT_ENTER, main.show_preview)
        self.step.Bind(wx.EVT_SPINCTRL, main.show_preview)

        self.countByDir = wx.CheckBox(id=wxID_PANELCOUNTBYDIR,
									  label=_(u"By directory"), name=u'countByDir', parent=self,
									  style=0)
        self.countByDir.SetToolTipString(_(u"Only change count when directory changes"))
        self.countByDir.SetValue(False)
        self.countByDir.Bind(wx.EVT_CHECKBOX, main.show_preview)

        self.staticText7 = wx.StaticText(id=wxID_PANELSTATICTEXT7,
										 label=_(u"Count by:"), name=u'staticText7', parent=self, style=0)

        self.asc = wx.RadioButton(id=wxID_PANELASC, label=_(u"+"), name=u'asc',
								  parent=self, style=wx.RB_GROUP)
        self.asc.SetFont(wx.Font(17, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        self.asc.SetValue(True)
        self.asc.SetToolTipString(_(u"Increase counting number"))
        self.asc.Bind(wx.EVT_RADIOBUTTON, main.show_preview)

        self.desc = wx.RadioButton(id=wxID_PANELDESC, label=_(u"-"),
								   name=u'desc', parent=self, style=0)
        self.desc.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD, False,
						  u'Impact'))
        self.desc.SetValue(False)
        self.desc.SetToolTipString(_(u"Decrease counting number"))
        self.desc.Bind(wx.EVT_RADIOBUTTON, main.show_preview)

        self.staticText6 = wx.StaticText(id=wxID_PANELSTATICTEXT6,
										 label=_(u"Count:"), name=u'staticText6', parent=self, style=0)

        self.start = wx.SpinCtrl(id=wxID_PANELSTART, initial=0, max=100000000,
								 min=0, name=u'start', parent=self, size=wx.Size(70, -1),
								 style=wx.SP_ARROW_KEYS)
        self.start.SetValue(1)
        self.start.SetToolTipString(_(u"Starting value"))
        self.start.Bind(wx.EVT_TEXT_ENTER, main.show_preview, id=wxID_PANELSTART)
        self.start.Bind(wx.EVT_SPINCTRL, main.show_preview, id=wxID_PANELSTART)

        self.startByItems = wx.CheckBox(id=wxID_PANELSTARTBYITEMS,
										label=_(u"Number of items"), name=u'startByItems', parent=self,
										style=0)
        self.startByItems.SetValue(False)
        self.startByItems.SetToolTipString(_(u"Use the number of items as the start value"))
        self.startByItems.Bind(wx.EVT_CHECKBOX, self._on_startbyitems_checkbox,
							   id=wxID_PANELSTARTBYITEMS)

        self.staticText1 = wx.StaticText(id=wxID_PANELSTATICTEXT1,
										 label=_(u"Reset every:"), name=u'staticText1', parent=self,
										 style=0)

        self.reset = wx.SpinCtrl(id=wxID_PANELRESET, initial=0, max=100000000,
								 min=1, name=u'reset', parent=self, size=wx.Size(70, -1),
								 style=wx.SP_ARROW_KEYS, value='0')
        self.reset.SetValue(1)
        self.reset.SetToolTipString(_(u"1 = don't reset"))
        self.reset.SetRange(1, 100000000)
        self.reset.Bind(wx.EVT_TEXT_ENTER, main.show_preview, id=wxID_PANELRESET)
        self.reset.Bind(wx.EVT_SPINCTRL, main.show_preview, id=wxID_PANELRESET)

        self.resetDir = wx.CheckBox(id=wxID_PANELRESETDIR,
									label=_(u"Directory"), name=u'resetDir', parent=self,
									style=0)
        self.resetDir.SetToolTipString(_(u"Reset count when directory changes"))
        self.resetDir.SetValue(False)
        self.resetDir.Bind(wx.EVT_CHECKBOX, main.show_preview)

        self.incrementOnDiff = wx.CheckBox(id=wxID_PANELRINCREMENTONDIFF,
										   label=_(u"Name change"), name=u'incrementOnDiff', parent=self,
										   style=0)
        self.incrementOnDiff.SetToolTipString(_(u"MUST be in LAST operation in stack !!"))
        self.incrementOnDiff.SetValue(False)
        self.incrementOnDiff.Bind(wx.EVT_CHECKBOX, main.show_preview)

        self.staticText3 = wx.StaticText(id=wxID_PANELSTATICTEXT3,
										 label=_(u"Repeat by:"), name=u'staticText1', parent=self,
										 style=0)

        self.repeat = wx.SpinCtrl(id=wxID_PANELREPEAT, initial=1, max=100000000,
								  min=1, name=u'reset', parent=self, size=wx.Size(70, -1),
								  style=wx.SP_ARROW_KEYS, value='1')
        self.repeat.SetValue(1)
        self.repeat.SetToolTipString(_(u"1 = don't repeat"))
        self.repeat.SetRange(1, 100000000)
        self.repeat.Bind(wx.EVT_TEXT_ENTER, main.show_preview,
						 id=wxID_PANELREPEAT)
        self.repeat.Bind(wx.EVT_SPINCTRL, main.show_preview, id=wxID_PANELREPEAT)

        self.__init_sizers()

    def __init__(self, parent, MainWindow):
        global main
        main = MainWindow
        self.__init_ctrls(parent)
        utils.set_min_size(self, ignoreClasses=(wx.TextCtrl, wx.SpinCtrl))
        self.on_config_load()

    def on_config_load(self):
        """Adjust after loading config."""
        self._check_styles(False)
        self.set_number_params(False)

    def set_number_params(self, event):
        """Determine parameters."""
        #ascending:
        if self.asc.GetValue() == True:
            stepDirection = + int(self.step.GetValue())
        #descending:
        else:
            stepDirection = -int(self.step.GetValue())

        start = self.start.GetValue()
        repeat = self.repeat.GetValue()-1
        reset = self.reset.GetValue()-1

        if repeat > 0 and reset == 0:
            maxNumb = abs((len(main.items) + (start-1)) * stepDirection) / (repeat + 1)
        elif repeat <= 0 and reset == 0:
            maxNumb = abs((len(main.items) + (start-1)) * stepDirection)
        elif reset != 0:
            maxNumb = reset

        # start at number of items
        if self.startByItems.GetValue():
            start = len(main.items)

        # alpha auto pad start value correction
        elif self.alpha.GetValue() and self.alphaPad.GetValue():
            def __to_alpha(i):
                s = ""
                while i:
                    i -= 1
                    q, m = divmod(i, 26)
                    s = chr(97 + m) + s
                    i = q
                return s
            width = len(__to_alpha(abs(maxNumb)))

            if width == 1:
                start = start
            elif width == 2 and start < 27:
                start = 26 + start
            elif width == 3 and start < 703:
                start = 702 + start
            elif width == 4 and start < 18279:
                start = 18278 + start

        self.Params = (start, stepDirection, reset,
					   self.resetDir.GetValue(), self.countByDir.GetValue(),
					   repeat, maxNumb)

    def _check_styles(self, event):
        """Enable or disable options based on what is selected."""
        #digit:
        digit_options = (self.digit_pad, self.pad_char, self.digitSetpad,
						 self.digit_autopad, self.padWidth)
        pad_options = (self.digitSetpad, self.digit_autopad, self.pad_char,
					   self.padWidth)
        if self.digit.GetValue():
            self.digit_pad.Enable(True)
            if self.digit_pad.GetValue():
                for option in pad_options:
                    option.Enable(True)
            else:
                for option in pad_options:
                    option.Enable(False)
            if self.reset.GetValue() == 4999:
                self.reset.SetValue(0)
            pad = self.digit_pad.GetValue()
            pad_char = self.pad_char.GetValue()
            if self.digitSetpad.GetValue():
                padWidth = self.padWidth.GetValue()
            else:
                padWidth = u"auto"
            self.Style = (u"digit", pad_char, padWidth, pad)
        else:
            for option in digit_options:
                option.Enable(False)

        #roman numeral:
        if self.roman.GetValue():
            self.roman_uc.Enable(True)

            if self.reset.GetValue() > 4999:
                self.reset.SetValue(4999)
            if self.start.GetValue() == 0:
                self.start.SetValue(1)

            self.Style = (u"roman", self.roman_uc.GetValue())
        else:
            self.roman_uc.Enable(False)

        #alphabetical:
        if self.alpha.GetValue():
            self.alphaUc.Enable(True)
            self.alphaPad.Enable(True)

            if self.start.GetValue() == 0:
                self.start.SetValue(1)
            if self.reset.GetValue() == 4999:
                self.reset.SetValue(0)

            self.Style = (u"alpha", self.alphaUc.GetValue(),
						  self.alphaPad.GetValue())
        else:
            self.alphaUc.Enable(False)
            self.alphaPad.Enable(False)
        main.show_preview(event)


    def _on_startbyitems_checkbox(self, event):
        if self.startByItems.GetValue():
            self.start.Enable(False)
        else:
            self.start.Enable(True)
        main.show_preview(event)

    def _on_padwidth_spinctrl(self, event):
        self.digitSetpad.SetValue(True)
        self._check_styles(event)
