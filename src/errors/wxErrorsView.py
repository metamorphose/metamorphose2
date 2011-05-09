# -*- coding: utf-8 -*-
#
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
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

[wxID_ERRORPANEL, wxID_ERRORPANELERRORSLIST, wxID_ERRORPANELERRORSSTATICTEXT1,
	wxID_ERRORPANELERRORSREMOVEERRORS, wxID_ERRORPANELERRORSREMOVEWARNINGS,
	wxID_ERRORPANELERRORSSTATICTEXT2, wxID_ERRORPANELERRORSREMOVE, wxID_ERRORPANELERRORSSAVE
] = [wx.NewId() for __init_ctrls in range(8)]

class ErrorList(wx.ListCtrl, ListCtrlAutoWidthMixin):
    """List control for errors."""
    
    def __init__(self, parent, ID, pos=wx.DefaultPosition):
        style = wx.LC_REPORT | wx.LC_VIRTUAL
        wx.ListCtrl.__init__(self, parent, ID, pos, wx.DefaultSize, style)
        # causes freeze under winXP
        #ListCtrlAutoWidthMixin.__init__(self)
        self.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT, heading=_(u"Error"),
						  width=260)
        self.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT, heading=_(u"File"),
						  width=639)
        imgs = wx.ImageList(16, 16)
        imgs.Add(wx.Bitmap(utils.icon_path(u'warn.ico'), wx.BITMAP_TYPE_ICO))
        imgs.Add(wx.Bitmap(utils.icon_path(u'failed.ico'), wx.BITMAP_TYPE_ICO))
        self.AssignImageList(imgs, wx.IMAGE_LIST_SMALL)
        self.SetItemCount(0)
        self.parent = parent

    def get_item(self, item):
        return self.parent.errorLog[int(item)]

    # overloads built in method
    def OnGetItemText(self, item, col):
        item = self.get_item(item)
        if col == 0:
            return item[2]
        else:
            return item[1]

    # overloads built in method
    def OnGetItemImage(self, item):
        item = self.get_item(item)
        if item[3] == 'warn':
            return 0
        else:
            return 1


class Panel(wx.Panel):
    """Error panel view"""
    
    def __init_sizer(self):
    	mainSizer = wx.BoxSizer(wx.VERTICAL)
    	options = wx.BoxSizer(wx.HORIZONTAL)
        options.Add(self.saveToLog, 0, wx.LEFT, 10)
    	options.Add(self.remove, 0, wx.LEFT, 215)
    	options.Add(self.staticText1, 0, wx.ALIGN_CENTER | wx.LEFT, 5)
    	options.Add(self.removeWarnings, 0, wx.ALIGN_CENTER | wx.LEFT, 5)
    	options.Add(self.removeErrors, 0, wx.ALIGN_CENTER | wx.LEFT, 5)
    	options.Add(self.staticText2, 0, wx.ALIGN_CENTER | wx.LEFT, 10)

        mainSizer.Add(self.errorsList, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 3)
        mainSizer.Add(options, 0, wx.BOTTOM, 3)

        self.SetSizerAndFit(mainSizer)


    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_ERRORPANEL, name=u'errorPanel',
						  parent=prnt, pos=wx.Point(295, 251), size=wx.Size(650, 302),
						  style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(642, 273))

        self.errorsList = ErrorList(self, wxID_ERRORPANELERRORSLIST)
        self.errorsList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_activate_error,
							 id=wxID_ERRORPANELERRORSLIST)

        self.staticText1 = wx.StaticText(id=wxID_ERRORPANELERRORSSTATICTEXT1,
										 label=_(u"items with:"), name=u'staticText1', parent=self, style=0)

        self.saveToLog = wx.Button(id=wxID_ERRORPANELERRORSSAVE, name=u'remove',
								   parent=self, label=_(u"Save errors to log"), style=wx.BU_EXACTFIT)
        self.saveToLog.SetToolTipString(_(u"Save errors to a log file."))
        self.saveToLog.Bind(wx.EVT_BUTTON, self.save_errors_to_log)
        self.saveToLog.Enable(False)

        self.remove = wx.Button(id=wxID_ERRORPANELERRORSREMOVE, name=u'remove',
								parent=self, label=_(u"Remove"), style=wx.BU_EXACTFIT)
        self.remove.SetToolTipString(_(u"Remove items from renaming selection"))
        self.remove.Bind(wx.EVT_BUTTON, self.remove_names_by_type)

        self.removeWarnings = wx.CheckBox(id=wxID_ERRORPANELERRORSREMOVEWARNINGS, label=_(u"warnings"),
										  name=u'removeWarnings', parent=self, style=0)
        self.removeWarnings.SetValue(False)
        self.removeWarnings.SetToolTipString(_(u"all items with warnings"))

        self.removeErrors = wx.CheckBox(id=wxID_ERRORPANELERRORSREMOVEERRORS, label=_(u"errors"),
										name=u'removeErrors', parent=self, style=0)
        self.removeErrors.SetValue(True)
        self.removeErrors.SetToolTipString(_(u"all items with errors"))

        self.staticText2 = wx.StaticText(id=wxID_ERRORPANELERRORSSTATICTEXT2,
										 label=_("from above items."), name=u'staticText1', parent=self, style=0)


    def __init__(self, Core, parent, main_window):
    	global main
        main = main_window

        self.__init_ctrls(parent)
        # adjust button sizes
        utils.adjust_exact_buttons(self)
        self.__init_sizer()

        # to store for removal
        self.errors = []
        self.warnings = []

        #print self.GetParent().GetEffectiveMinSize()
        #width = self.GetSize()[0]
        #self.errorsList.SetColumnWidth(1, width-200)


    def display_errors(self, errorLog, warn, bad):
        self.errorLog = errorLog
        self.errorsList.SetItemCount(len(errorLog))
        
        for error in errorLog:
            #if not (error[0] in warn and error[0] in bad) or error[3] == u'bad':
            if error[3] == 'bad':
                self.errors.append(error[1])
            else:
                self.warnings.append(error[1])

        badCount = len(self.errors)
        warnCount = len(self.warnings)

        main.notebook.SetPageText(3, _(u"Errors: %s - Warnings: %s") % (badCount, warnCount))

        if len(warn) != 0 and len(bad) == 0:
            main.set_status_msg(_(u"Ready to rename %s items, but with %s warnings") % (len(main.toRename), warnCount), u'warn')
            self.saveToLog.Enable(False)
        else:
            main.set_status_msg(_(u"%s total items, %s have problems") % (len(main.toRename), badCount + warnCount), u'failed')
            self.saveToLog.Enable(True)

    def clear_errors(self):
        self.errors = []
        self.warnings = []
        self.errorsList.DeleteAllItems()
        self.saveToLog.Enable(False)
        main.notebook.SetPageText(3, _(u"Errors/Warnings: 0"))

    def on_activate_error(self, event):
        currentItem = event.m_itemIndex
        item_numb = self.errorsList.GetItemData(currentItem)
        main.bottomWindow.display.EnsureVisible(item_numb)

    def remove_names_by_type(self, event):
        """remove errors from renaming selection"""
        if self.removeErrors.GetValue():
            self.remove_names(self.errors)
        if self.removeWarnings.GetValue():
            self.remove_names(self.warnings)
        main.picker.enable_buttons()
        main.show_preview(event)

    def remove_names(self, namesToremove):
        main.picker.remove_items_by_name(namesToremove)

    def save_errors_to_log(self, event):
        CSVfile = u''
        #for i in range(self.errorsList.GetItemCount()):
        #    item = self.errorsList.GetItem(i)
        #    CSVfile += u'"%s"\n' % item.GetData()
        for item in self.errors:
            CSVfile += u'"%s"\n' % item
        dlg = wx.FileDialog(self, message=_(u"Save error list as ..."),
							defaultDir='', defaultFile=u'.csv',
							wildcard=_(u"Log file (*.csv)") + u'|*.csv',
							style=wx.SAVE | wx.OVERWRITE_PROMPT
							)
        if dlg.ShowModal() == wx.ID_OK:
            # attempt to write file
            utils.write_file(dlg.GetPath(), CSVfile)
        dlg.Destroy()
