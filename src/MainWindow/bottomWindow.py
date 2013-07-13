# -*- coding: utf-8 -*-
#
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

"""
The bottom half of the main window.
"""
import os

import app
import editDialog
import utils
import wx
import wx.lib.buttons as buttons

[
wxID_BOTTOM_WINDOW, wxID_AUTOPREVIEW, wxID_GO,
wxID_MENUEDIT, wxID_MENUREMOVE, wxID_MENUREMOVEANDPREVIEW,
wxID_THUMBSIZE, wxID_AUTOPREVIEW,
wxID_IMGPREVIEW, wxID_UNDOREDO,
] = [wx.NewId() for _init_coll_menuEdit_Items in range(10)]

class ListCtrl(wx.ListCtrl):
    """Bottom preview virtual listcrtl."""

    def __init__(self, parent, id, pos=wx.DefaultPosition,
				 size=wx.DefaultSize):
        self.parent = parent.GetGrandParent()
        wx.ListCtrl.__init__(self, parent, id, pos, size,
							 style=wx.LC_REPORT | wx.LC_VIRTUAL)
        self.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
						  heading=_(u"Location"), width=225)
        self.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
						  heading=_(u"Original Name"), width=245)
        self.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT,
						  heading=_(u"New Name"), width=265)
        self.SetMinSize(wx.Size(-1, 110))
        self.SetItemCount(0)
        self.showDirs = False
        self.mode = 'preview'
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self._on_right_click)
        self.set_preferences()

    def set_preferences(self):
        prefs = app.prefs
        self.green = wx.ListItemAttr()
        self.green.SetBackgroundColour(prefs.get(u'renamedColor'))
        self.lightGreen = wx.ListItemAttr()
        self.lightGreen.SetBackgroundColour(prefs.get(u'willChangeColor'))
        self.red = wx.ListItemAttr()
        self.red.SetBackgroundColour(prefs.get(u'errorColor'))
        self.yellow = wx.ListItemAttr()
        self.yellow.SetBackgroundColour(prefs.get(u'warnColor'))

    def __init_menu(self, menu):
        """Right click menu."""
        menu.edit = wx.MenuItem(menu, wxID_MENUEDIT, _(u"Manually Edit"))
        menu.edit.SetBitmap(wx.Bitmap(utils.icon_path(u'edit.png'),
							wx.BITMAP_TYPE_PNG))

        menu.remove = wx.MenuItem(menu, wxID_MENUREMOVE, _(u"Remove Item(s)"))
        menu.remove.SetBitmap(wx.Bitmap(utils.icon_path(u'errors.png'),
							  wx.BITMAP_TYPE_PNG))

        menu.removeAndPreview = wx.MenuItem(menu, wxID_MENUREMOVEANDPREVIEW,
											_(u"Remove Item(s) and preview"))
        menu.removeAndPreview.SetBitmap(wx.Bitmap(utils.icon_path(u'errors.png'),
										wx.BITMAP_TYPE_PNG))

        menu.AppendItem(menu.edit)
        menu.AppendItem(menu.remove)
        menu.AppendItem(menu.removeAndPreview)
        #menu.AppendItem(parent.disable)

        self.Bind(wx.EVT_MENU, self._remove_items,
				  id=wxID_MENUREMOVE)
        self.Bind(wx.EVT_MENU, self._remove_items_and_preview,
				  id=wxID_MENUREMOVEANDPREVIEW)
        self.Bind(wx.EVT_MENU, self._manual_edit,
				  id=wxID_MENUEDIT)

    def _on_right_click(self, event):
        """Popup the right click menu."""
        if hasattr(self.parent, 'toRename') and len(self.parent.toRename) != 0:
            self.rightClickMenu = wx.Menu()
            self.__init_menu(self.rightClickMenu)
            self.PopupMenu(self.rightClickMenu)

    def _remove_items(self, event):
        """Remove selected items, needs renaming list adjusted afterwards."""
        itemNames = []
        item = -1
        while True:
            item = self.GetNextItem(item, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
            itemName = self.parent.toRename[item][0][0]
            if item == -1:
                break
            else:
                itemNames.append(itemName)
            self.parent.toRename.pop(item)
        self.parent.picker.remove_items_by_name(itemNames)
        self.DeleteAllItems()
        self.SetItemCount(len(self.parent.toRename))

    def _remove_items_and_preview(self, event):
        self._remove_items(event)
        self.parent.on_preview_button(False)

    def _remove_items_and_error_check(self, event):
        self._remove_items()
        self.parent.renamer.error_check_items()

    def _manual_edit(self, event):
        """Allow editing single item manually."""
        item = self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)

        self.dlg = editDialog.Dialog(self, item)

        if self.dlg.ShowModal() == wx.ID_OK:
            self.set_name(self.dlg.item, self.dlg.get_value())

    def _get_preview_attr(self, item):
        original, renamed = self.get_names(item)
        # make bad/warn names stand out
        if item in self.parent.bad:
            return self.red
        elif item in self.parent.warn:
            return self.yellow
        # make items that will be renamed stand out
        elif app.prefs.get('showPreviewHighlight') and\
			(original[0] != renamed[0]):
				return self.lightGreen
        else:
            return None

    def _get_rename_attr(self, item):
        original, renamed = self.get_names(item)
        if renamed[1] == False:
            return None
        elif renamed[1] and (original[0] != renamed[0]):
            return self.green
        elif renamed[1] == None:
            return self.red

    def set_name(self, item, new):
        """Set a new name manually."""
        if new:
            self.parent.toRename[item][1][0] = new
            self.parent.renamer.error_check_items()

    def set_item_selected(self, item):
        self.EnsureVisible(item)
        self.SetItemState(item, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

    def set_item_deselected(self, item):
        self.SetItemState(item, 0, wx.LIST_STATE_SELECTED | wx.LIST_STATE_FOCUSED)

    def get_names(self, item):
        """Get the info for an item from the list."""
        item = self.parent.toRename[int(item)]
        original = item[0]
        renamed = item[1]
        return original, renamed

    # overloads built in method
    def OnGetItemAttr(self, item):
        if self.mode == 'preview':
            return self._get_preview_attr(item)
        elif self.mode == 'rename':
            return self._get_rename_attr(item)

    # overloads built in method
    def OnGetItemText(self, item, col):
        original, renamed = self.get_names(item)
        split = os.path.split(original[0])
        if self.showDirs:
            to_rename = renamed[0].lstrip(os.path.sep)
        else:
            to_rename = os.path.split(renamed[0])[1]
        if col == 0:
            return split[0]
        elif col == 1:
            return split[1]
        else:
            return to_rename

    # overloads built in method
    def OnGetItemImage(self, item):
        pickerList = self.parent.picker.view.ItemList
        original, renamed = self.get_names(item)
        if original[1]:
            # show preview if available
            if app.prefs.get('showPreviewIcons') and\
				pickerList.thumbnails.has_key(original[0]):
					img = pickerList.thumbnails[original[0]]
            else:
                img = 1
        else:
            img = 0
        return img



class MainPanel(wx.Panel):
    """
    The bottom panel of the main splitter.
    """
    def __init_sizer(self):
        buttonSizer = self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer.AddWindow(self.preview, 0, wx.LEFT, 10)
        buttonSizer.AddWindow(self.go, 0, wx.LEFT, 10)
        buttonSizer.AddSpacer((-1, 25), 1)
        buttonSizer.AddWindow(self.imgPreview, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        buttonSizer.AddWindow(self.thumbSize, 0, wx.ALIGN_CENTER | wx.RIGHT, 15)
        buttonSizer.AddWindow(self.autoPreview, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
        mainSizer.AddSizer(buttonSizer, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.TOP, 5)
        mainSizer.AddWindow(self.display, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizerAndFit(mainSizer)


    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_BOTTOM_WINDOW, name=u'Panel',
						  parent=prnt, style=wx.TAB_TRAVERSAL)


        self.display = ListCtrl(self, -1, size=wx.Size(520, -1))

        #self.display.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.main.on_item_selected,
        #                  self.display)

        self.display.Bind(wx.EVT_LIST_ITEM_SELECTED, self.main.on_item_selected,
						  self.display)

        self.preview = buttons.GenBitmapTextButton(self, wxID_AUTOPREVIEW,
												   wx.Bitmap(utils.icon_path(u'preview.png'),
												   wx.BITMAP_TYPE_PNG), _(u"Preview"), size=(-1, 26))
        self.Bind(wx.EVT_BUTTON, self.main.on_preview_button,
				  id=wxID_AUTOPREVIEW)

        self.go = buttons.GenBitmapTextButton(self, wxID_GO,
											  wx.Bitmap(utils.icon_path(u'go.png'), wx.BITMAP_TYPE_PNG),
											  _(u"Go!"), size=(-1, 26))
        self.go.Enable(False)
        self.go.Bind(wx.EVT_BUTTON, self.main.rename_items, id=wxID_GO)

        self.imgPreview = wx.CheckBox(id=wxID_IMGPREVIEW,
									  label=_(u"Show image thumbnails"), name=u'imgPreview', parent=self,
									  style=0)
        self.imgPreview.SetToolTipString(_(u"Can slow preview considerably"))
        self.imgPreview.SetValue(False)
        self.imgPreview.Bind(wx.EVT_CHECKBOX, self.__refresh_picker)

        self.thumbSize = wx.Choice(id=wxID_THUMBSIZE,
								   choices=[u'32', u'64', u'128', u'256'],
								   name=u'dirsPlace', parent=self, size=wx.Size(62, -1),
								   style=0)
        self.thumbSize.SetSelection(1)
        self.thumbSize.SetToolTipString(_(u"Thumbnail Size"))
        self.thumbSize.Bind(wx.EVT_CHOICE, self.__set_thumb_size)

        if not utils.is_pil_loaded():
            self.imgPreview.SetValue(False)
            self.imgPreview.Enable(False)
            self.thumbSize.Enable(False)

        self.autoPreview = wx.CheckBox(id=wxID_AUTOPREVIEW,
									   label=_(u"Automatic Preview"), name=u'autoPreview', parent=self,
									   style=0)
        self.autoPreview.SetToolTipString(_(u"Disable when working with many items"))
        self.autoPreview.SetValue(True)


    def __init__(self, prnt, MainWindow):
        self.main = MainWindow
        self.__init_ctrls(prnt)
        self.__init_sizer()
        self.__create_undo_redo(_("Undo"))
        # disable if no undo files exist (to lessen user confusion)
        if not os.path.exists(utils.get_user_path(u'undo/original.bak')) or not\
			os.path.exists(utils.get_user_path(u'undo/renamed.bak')):
				self.undoRedo.Enable(False)

    def __refresh_picker(self, event):
        self.main.picker.refresh(event)

    def __set_thumb_size(self, event):
        """Only re-preview if image preview is enabled and size has changed."""
        if hasattr(self.main.picker.view.ItemList, 'thumbSize'):
            thumbSize = self.main.picker.view.ItemList.thumbSize[0]
        else:
            thumbSize = int(event.GetString())
        if self.imgPreview.GetValue() and int(event.GetString()) != thumbSize:
            self.__refresh_picker(event)

    def __create_undo_redo(self, label):
        """Deletes and creates a new button, hack to change image."""
        if label == _("Undo"):
            img = wx.Bitmap(utils.icon_path(u'undo.ico'), wx.BITMAP_TYPE_ICO)
        else:
            img = wx.Bitmap(utils.icon_path(u'redo.ico'), wx.BITMAP_TYPE_ICO)
        if hasattr(self, 'undoRedo'):
            self.undoRedo.Destroy()
        self.undoRedo = buttons.GenBitmapTextButton(self, wxID_UNDOREDO, img, label, size=(-1, 26))
        # do not use wx.EVT_BUTTON, causes seg fault
        self.undoRedo.Bind(wx.EVT_LEFT_DOWN, self.main.undo_rename, id=wxID_UNDOREDO)
        self.buttonSizer.Insert(2, self.undoRedo, proportion=0, flag=wx.LEFT, border=25)
        self.Layout()

    def set_undo_redo_type(self, op):
        if op == 'check':
            if self.undoRedo.GetLabel() == _("Undo"):
                self.__create_undo_redo(_("Redo"))
            else:
                self.__create_undo_redo(_("Undo"))
        elif op == 'undo':
            self.__create_undo_redo(_("Undo"))

    def set_preferences(self):
        self.display.set_preferences()