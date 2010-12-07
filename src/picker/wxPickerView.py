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
wxWidgets picker panel and associated classes.
Only responsible for views, All interactions must be handled by picker Core
"""

import wx
import utils
import os
try:
    import Image
except:
    utils.make_err_msg(_("Python Imaging Library (PIL) not found.\nRefer to readme file for install instructions.\n\nYou will not be able to preview images."),
                     _("PIL needed"))

[wxID_PICKERPANEL, wxID_PICKERPANELBROWSE, wxID_SELECTIONAREADIRPICKER,
 wxID_PICKERPANELDIVIDER1, wxID_PICKERPANELFILESON,
 wxID_PICKERPANELFILTERSEL, wxID_PICKERPANELFOLDERSON, wxID_PICKERPANELNOT_TYPE,
 wxID_PICKERPANELOK, wxID_PICKERPANELPATH, wxID_PICKERPANELPATH_HELP,
 wxID_SELECTIONAREAFPICKER, wxID_PICKERPANELSELECT, wxID_PICKERPANELSELECT_ALL,
 wxID_PICKERPANELSELECT_NONE, wxID_PICKERPANELSTATICTEXT1,
 wxID_PICKERPANELWALKIT, wxID_PICKERPANELFILTERBYRE, wxID_SELECTIONAREA,
 wxID_PICKERPANELIGNORECASE, wxID_PICKERPANELUSELOCALE, wxID_PICKERPANELWALKDEPTH,
 wxID_PICKERPANELSTATICTEXT2,
] = [wx.NewId() for __init_ctrls in range(23)]


# Panel refers to instance as dirpicker
class DirectoryList(wx.GenericDirCtrl):
    def __init__(self, parent, ID, name, showHidden):
        self.parent = parent.GetParent()
        wx.GenericDirCtrl.__init__(self, parent, ID, name,
          defaultFilter=0, filter='', style=wx.DIRCTRL_DIR_ONLY)

        if showHidden:
            self.ShowHidden(True)

        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        # closed folder:
        il.Add(wx.Bitmap(utils.icon_path(u'folder16.png'),wx.BITMAP_TYPE_PNG))
        # open folder:
        il.Add(wx.Bitmap(utils.icon_path(u'folderOpen.png'),wx.BITMAP_TYPE_PNG))
        # root of filesystem (linux):
        il.Add(wx.Bitmap(utils.icon_path(u'root.ico'),wx.BITMAP_TYPE_ICO))
        # drive letter (windows):
        il.Add(wx.Bitmap(utils.icon_path(u'hdd.ico'),wx.BITMAP_TYPE_ICO))
        # cdrom drive:
        il.Add(wx.Bitmap(utils.icon_path(u'cdrom.ico'),wx.BITMAP_TYPE_ICO))
        # removable drive on win98:
        il.Add(wx.Bitmap(utils.icon_path(u'fdd.ico'),wx.BITMAP_TYPE_ICO))
        # removable drive (floppy, flash, etc):
        il.Add(wx.Bitmap(utils.icon_path(u'fdd.ico'),wx.BITMAP_TYPE_ICO))
        self.il = il
        self.GetTreeCtrl().SetImageList(il)
        self.bind()

    def dir_change(self,event):
        self.parent.path.SetValue(self.GetPath())
        self.parent._refresh_items(event)

    def unbind(self):
        self.Bind(wx.EVT_TREE_SEL_CHANGED, utils.dev_null)

    def bind(self):
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.dir_change)

    def refresh_tree(self):
        itemId = self.GetTreeCtrl().GetSelection()
        self.GetTreeCtrl().CollapseAndReset(itemId)
        self.GetTreeCtrl().Expand(itemId)


class ItemList(wx.ListCtrl):
    """Picker list and associated functions."""

    def __init__(self, parent, id, name, MainWindow):
        self.pickerPanel = parent.GetParent()

        global main
        main = MainWindow

        style = wx.LC_LIST
        #style = wx.LC_REPORT|wx.LC_NO_HEADER|wx.LC_VIRTUAL

        wx.ListCtrl.__init__(self, parent, id=id, name=name, style=style)
        self.thumbnails = {}
        self._create_image_list(main.bottomWindow.imgPreview.GetValue())

        """
        self.SetItemCount(100000)
        self.InsertColumn(0, "First")
        self.SetColumnWidth(0, 470)

        self.attr1 = wx.ListItemAttr()
        self.attr1.SetBackgroundColour("yellow")

        self.attr2 = wx.ListItemAttr()
        self.attr2.SetBackgroundColour("light blue")

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)
        """
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        self.Bind(wx.EVT_KEY_DOWN, self._on_key_down)
        self.Bind(wx.EVT_KEY_UP, self._on_key_up)

        # keep shift key value
        self.shiftDown = False
        self.totalSelected = 0

    def _create_image_list(self, imgPreview):
        # get thumbnail size
        if imgPreview:
            xy = int(main.bottomWindow.thumbSize.GetStringSelection())
            thumbSize=(xy,xy)
        else:
            thumbSize=(16,16)
        # apply to list
        self.imgs = wx.ImageList(thumbSize[0],thumbSize[1])
        self.folderIco = self.imgs.Add(wx.Bitmap(utils.icon_path(u'folder%s.png'%thumbSize[0]),
           wx.BITMAP_TYPE_PNG))
        self.fileIco = self.imgs.Add(wx.Bitmap(utils.icon_path(u'file%s.png'%thumbSize[0]),
           wx.BITMAP_TYPE_PNG))
        self.SetImageList(self.imgs, wx.IMAGE_LIST_SMALL)
        return thumbSize

    def _get_item_info(self, item):
        """Get item info and parse it for inclusion in renaming list."""
        item_txt = self.GetItemText(item)
        item_txt = item_txt.lstrip(os.sep)
        fullItem = os.path.join(self.pickerPanel.path.GetValue(),item_txt)
        IsFile = os.path.isfile(fullItem)
        fullItem = [fullItem,IsFile]
        return fullItem

    def _on_key_down(self, event):
        """Need to know if shift is pressed to adjust selection."""
        if event.m_keyCode == wx.WXK_SHIFT:
            self.shiftDown = True
        else:
            self.shiftDown = False

    def _on_key_up(self, event):
        self.shiftDown = False
        if event.m_keyCode == wx.WXK_SHIFT:
            self.totalSelected = 0
            self.pickerPanel.enable_buttons()
            main.show_preview(True)
    
    def _image_to_pil(self, source, thumbSize):
        """Create a thumbnail from an image file."""
        source = Image.open(source, 'r')
        source.thumbnail(thumbSize, Image.ANTIALIAS)
        image = apply(wx.EmptyImage, source.size)
        image.SetData(source.convert("RGB").tostring())
        return wx.BitmapFromImage(image)

    def on_item_selected(self, event):
        """show selected items then add or remove from renaming list."""
        currentItem = event.m_itemIndex
        item = wx.ListItem()
        item.SetId(currentItem)
        fullItem = self._get_item_info(currentItem)

        # avoid selecting same item twice when using shift key
        if self.shiftDown:
            self.totalSelected += 1

        if self.totalSelected != 1:
            # add to list / show selected:
            if fullItem not in self.pickerPanel.Core.joinedItems:
                item.SetBackgroundColour(main.prefs.get(u'highlightColor'))
                item.SetTextColour(main.prefs.get(u'highlightTextColor'))
                self.pickerPanel.Core.joinedItems.append(fullItem)
            # remove from list / show deselected:
            else:
                item.SetBackgroundColour(main.prefs.get(u'backgroundColor'))
                item.SetTextColour(main.prefs.get(u'textColor'))
                self.pickerPanel.Core.joinedItems.remove(fullItem)
            # apply highlighting
            self.SetItem(item)

        if len(main.renamer.operations) == 0:
            msg = _(u"%s items were (de)selected") % (self.totalSelected+1)
            main.set_status_msg(msg, 'eyes')

        # Deselect item to avoid user confusion
        main.currentItem = None
        self.Select(currentItem, False)

        if not self.shiftDown:
            self.pickerPanel.enable_buttons()
            main.show_preview(True)


    def add_items(self, root, folders, files):
        """Add items found to list."""
        self.thumbnails = {}
        supported = ('.png','.jpg','.bmp','.tif','.jpeg',
                     '.tiff','.gif','.ico','.thm')
        imgPreview = main.bottomWindow.imgPreview.GetValue()
        thumbSize = self.thumbSize = self._create_image_list(imgPreview)

        if imgPreview and utils.is_pil_loaded():
            imgPreview = True
            def _get_ext(item):
                return os.path.splitext(item)[1].lower()
        else:
            imgPreview = False

        # list folders first
        folders.sort(key=lambda x: x.lower())
        for i in range(len(folders)):
            self.InsertImageStringItem(i, folders[i], 0)

        # ... then files
        def _make_key(f): return (os.path.dirname(f), f.lower())
        files.sort(key=_make_key)

        i = len(folders)
        for item in files:
            # preview images
            if imgPreview is True and _get_ext(item) in supported:
                fullitem = os.path.join(root,item.lstrip('/'))
                try:
                    thumb = self._image_to_pil(fullitem,thumbSize)

                except IOError:
                    img = 1
                else:
                    img = self.imgs.Add(thumb)
                    # link name with number in imageList for main window
                    self.thumbnails[fullitem] = img
            else:
                img = 1
            self.InsertImageStringItem(i, item, img)
            i += 1

    """
    def OnItemActivated(self, event):
        self.currentItem = event.m_itemIndex
        self.log.WriteText("OnItemActivated: %s\nTopItem: %s\n" %
                           (self.GetItemText(self.currentItem), self.GetTopItem()))


    def OnItemDeselected(self, evt):
        print self.items[evt.m_itemIndex]
        #print "OnItemDeselected: %s" % evt.m_itemIndex

    #---------------------------------------------------
    # These methods are callbacks for implementing the
    # "virtualness" of the list...  Normally you would
    # determine the text, attributes and/or image based
    # on values from some external data source, but for
    # this demo we'll just calculate them
    def on_get_item_text(self, item, col):
        return "Item %d, column %s" % (item, col)

    def on_get_item_image(self, item):
        return self.folderIco


    def OnGetItemAttr(self, item):
        if item % 3 == 1:
            return self.attr1
        elif item % 3 == 2:
            return self.attr2
        else:
            return None
    """


class Panel(wx.Panel):
    def __init_sizer(self):
        # adjust button sizes
        #utils.adjust_exact_buttons(self,ignore=('OK'))
        utils.adjust_exact_buttons(self)

        PathSizer = self.PathSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        SelectSizer = self.SelectSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        mainSizer = self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)

        PathSizer.AddWindow(self.BROWSE,0,wx.ALL, 5, wx.ALIGN_CENTER)
        PathSizer.AddWindow(self.path,1,wx.ALIGN_CENTER|wx.RIGHT, 5)
        PathSizer.AddWindow(self.walkIt,0,wx.ALIGN_CENTER|wx.RIGHT, 5)
        PathSizer.AddWindow(self.staticText2,0,wx.ALIGN_CENTER|wx.RIGHT, 3)
        PathSizer.AddWindow(self.walkDepth,0,wx.ALIGN_CENTER|wx.RIGHT, 15)
        PathSizer.AddWindow(self.OK,0,wx.RIGHT|wx.ALIGN_CENTER,8)

        SelectSizer.AddWindow(self.notType,0,wx.ALIGN_CENTER)
        SelectSizer.AddWindow(self.staticText1,0,wx.ALIGN_CENTER|wx.LEFT,3)
        SelectSizer.AddWindow(self.FilterSel,20,wx.ALIGN_CENTER)
        SelectSizer.AddWindow(self.filterByRE,0,wx.ALIGN_CENTER|wx.LEFT,5)
        SelectSizer.AddWindow(self.ignoreCase,0,wx.ALIGN_CENTER|wx.LEFT,2)
        SelectSizer.AddWindow(self.useLocale,0,wx.ALIGN_CENTER|wx.LEFT,2)
        SelectSizer.AddSpacer((-1,-1),1,wx.EXPAND)
        SelectSizer.AddWindow(self.divider1,0,wx.ALIGN_CENTER)
        SelectSizer.AddSpacer((-1,-1),1,wx.EXPAND)
        SelectSizer.AddWindow(self.select,0,wx.RIGHT|wx.ALIGN_CENTER,5)
        SelectSizer.AddWindow(self.foldersOn,0,wx.ALIGN_CENTER|wx.RIGHT,7)
        SelectSizer.AddWindow(self.filesOn,0,wx.ALIGN_CENTER|wx.RIGHT,5)
        SelectSizer.AddSpacer((-1,-1),1,wx.EXPAND)
        SelectSizer.AddWindow(self.selectAll,0,wx.RIGHT,2)
        SelectSizer.AddWindow(self.selectNone,0)
        SelectSizer.AddSpacer((-1,-1),1,wx.EXPAND)

        mainSizer.AddWindow(self.pathHelp,0,wx.EXPAND|wx.LEFT|wx.TOP, 6)
        mainSizer.AddSizer(PathSizer,0,wx.EXPAND|wx.ALIGN_CENTER)
        mainSizer.AddSizer(SelectSizer,0,wx.LEFT|wx.EXPAND,6)
        mainSizer.AddWindow(self.selectionArea,1,wx.EXPAND|wx.TOP, 3)

        self.SetSizerAndFit(mainSizer)

    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_PICKERPANEL, name=u'pickerPanel',
              parent=prnt, style=wx.NO_BORDER)

        self.path = wx.TextCtrl(id=wxID_PICKERPANELPATH, name=u'path',
              parent=self, style=wx.TE_PROCESS_ENTER, value='')
        self.path.Bind(wx.EVT_TEXT_ENTER, self.Core.set_path,
              id=wxID_PICKERPANELPATH)

        self.OK = wx.Button(id=wxID_PICKERPANELOK, label=_(u"Refresh"), name=u'OK',
              parent=self, style=wx.BU_EXACTFIT)
        #reloadImg = wx.Bitmap(utils.icon_path(u'reload.png'), wx.BITMAP_TYPE_PNG)
        #self.OK = wx.BitmapButton(bitmap=reloadImg, id=wxID_PICKERPANELOK, name=u'OK',
        #      parent=self, style=wx.BU_AUTODRAW)
        self.OK.Enable(True)
        self.OK.SetToolTipString(_(u"Load or reload current path"))
        self.OK.Bind(wx.EVT_BUTTON, self.Core.set_path, id=wxID_PICKERPANELOK)

        self.BROWSE = wx.Button(id=wxID_PICKERPANELBROWSE, label=_(u"Browse"),
          name=u'BROWSE', parent=self, style=wx.BU_EXACTFIT)
        self.BROWSE.SetToolTipString(_(u"Browse for path"))
        self.BROWSE.Bind(wx.EVT_BUTTON, self.browse_for_path,
          id=wxID_PICKERPANELBROWSE)

        self.pathHelp = wx.StaticText(id=wxID_PICKERPANELPATH_HELP,
              label=_(u"Input/Paste path and press OK, or BROWSE for path:"),
              name=u'pathHelp', parent=self, style=0)

        self.select = wx.StaticText(id=wxID_PICKERPANELSELECT, label=_(u"Select:"),
              name=u'select', parent=self, style=0)

        self.selectAll = wx.Button(id=wxID_PICKERPANELSELECT_ALL, label=_(u"all"),
              name=u'selectAll', parent=self, style=wx.BU_EXACTFIT)
        self.selectAll.Enable(False)
        self.selectAll.Bind(wx.EVT_BUTTON, self.select_all,
              id=wxID_PICKERPANELSELECT_ALL)

        self.selectNone = wx.Button(id=wxID_PICKERPANELSELECT_NONE,
              label=_(u"none"), name=u'selectNone', parent=self, style=wx.BU_EXACTFIT)
        self.selectNone.Enable(False)
        self.selectNone.Bind(wx.EVT_BUTTON, self.select_none,
              id=wxID_PICKERPANELSELECT_NONE)

        self.foldersOn = wx.CheckBox(id=wxID_PICKERPANELFOLDERSON, label=_(u"Folders"),
              name=u'foldersOn', parent=self, style=0,)
        self.foldersOn.SetValue(True)
        self.foldersOn.Bind(wx.EVT_CHECKBOX, self._refresh_items,
              id=wxID_PICKERPANELFOLDERSON)

        self.filesOn = wx.CheckBox(id=wxID_PICKERPANELFILESON, label=_(u"Files"),
              name=u'filesOn', parent=self, style=0)
        self.filesOn.SetValue(True)
        self.filesOn.Bind(wx.EVT_CHECKBOX, self._refresh_items,
              id=wxID_PICKERPANELFILESON)

        keys = self.get_in_searches()
        self.FilterSel = wx.ComboBox(choices=keys, id=wxID_PICKERPANELFILTERSEL,
              name=u'FilterSel', parent=self, style=wx.TE_PROCESS_ENTER)
        self.FilterSel.SetSelection(0)
        self.FilterSel.SetToolTipString(_(u"Names containing (Use menu or enter text)"))
        self.FilterSel.Bind(wx.EVT_COMBOBOX, self._on_filter_sel,
              id=wxID_PICKERPANELFILTERSEL)
        self.FilterSel.Bind(wx.EVT_TEXT_ENTER, self._refresh_items,
              id=wxID_PICKERPANELFILTERSEL)

        self.staticText1 = wx.StaticText(id=wxID_PICKERPANELSTATICTEXT1,
              label=_(u"Contaning:"), name=u'staticText1', parent=self, style=0)

        self.filterByRE = wx.CheckBox(id=wxID_PICKERPANELFILTERBYRE, label=_(u"Reg-Expr"),
              name=u'filterByRE', parent=self, style=0)
        self.filterByRE.SetValue(False)
        self.filterByRE.SetToolTipString(_(u"Evaluate filter as a regular expression"))
        self.filterByRE.Bind(wx.EVT_CHECKBOX, self.__regex_options,
              id=wxID_PICKERPANELFILTERBYRE)

        self.ignoreCase = wx.CheckBox(id=wxID_PICKERPANELIGNORECASE, label=_(u"I"),
              name=u'ignoreCase', parent=self, style=0)
        self.ignoreCase.SetValue(True)
        self.ignoreCase.Enable(False)
        self.ignoreCase.SetToolTipString(_(u"case-Insensitive match"))
        self.ignoreCase.Bind(wx.EVT_CHECKBOX, self._refresh_items,
              id=wxID_PICKERPANELIGNORECASE)

        self.useLocale = wx.CheckBox(id=wxID_PICKERPANELUSELOCALE, label=_(u"U"),
              name=u'useLocale', parent=self, style=0)
        self.useLocale.SetValue(True)
        self.useLocale.Enable(False)
        self.useLocale.SetToolTipString(_(u"Unicode match (\w matches 'a','b','c', etc)"))
        self.useLocale.Bind(wx.EVT_CHECKBOX, self._refresh_items,
              id=wxID_PICKERPANELUSELOCALE)

        self.walkIt = wx.CheckBox(id=wxID_PICKERPANELWALKIT, label=_(u"Recursive"),
              name=u'walkIt', parent=self, style=0)
        self.walkIt.SetValue(False)
        self.walkIt.SetToolTipString(_(u"Get all files in directory and sub-directories, but no folders"))
        self.walkIt.Bind(wx.EVT_CHECKBOX, self.__on_recursive_checkbox,
              id=wxID_PICKERPANELWALKIT)

        self.staticText2 = wx.StaticText(id=wxID_PICKERPANELSTATICTEXT2,
              label=_(u"depth:"), name=u'staticText2', parent=self, style=0)
        self.staticText2.Enable(False)

        self.walkDepth = wx.SpinCtrl(id=wxID_PICKERPANELWALKDEPTH, initial=0,
              max=999, min=0, name=u'walkDepth', parent=self,
              size=wx.Size(56, -1), style=wx.SP_ARROW_KEYS, value='0')
        self.walkDepth.SetValue(0)
        self.walkDepth.SetToolTipString(_(u"Number of levels to descend, 0 = unlimited"))
        self.walkDepth.Enable(False)

        self.notType = wx.CheckBox(id=wxID_PICKERPANELNOT_TYPE, label=_(u"Not"),
              name=u'notType', parent=self, style=0)
        self.notType.SetValue(False)
        self.notType.SetToolTipString(_(u"NOT containing"))
        self.notType.Bind(wx.EVT_CHECKBOX, self._refresh_items,
              id=wxID_PICKERPANELNOT_TYPE)

        self.divider1 = wx.StaticLine(id=wxID_PICKERPANELDIVIDER1,
              name=u'divider1', parent=self, size=wx.Size(3, 22), style=wx.LI_VERTICAL)

        # create split window:
        self.selectionArea = wx.SplitterWindow(parent=self, id=wxID_SELECTIONAREA,
          name=u'selectionArea', style=wx.SP_LIVE_UPDATE)

        # directory picker:
        if main.prefs.get(u'useDirTree'):
            self.__create_dir_tree()

        # file picker:
        self.ItemList = ItemList(id=wxID_SELECTIONAREAFPICKER, name=u'picker',
                                 parent=self.selectionArea,MainWindow=main)

        self.__init_splitter()


    def __init_splitter(self):
        """Initialise split window based on preferences."""
        if main.prefs.get('useDirTree'):
            self.selectionArea.SplitVertically(self.dirPicker, self.ItemList, 280)
        else:
            self.selectionArea.Initialize(self.ItemList)


    def __init__(self, Core, parent, MainWindow):
        global main
        main = MainWindow
        self.Core = Core
        self.__init_ctrls(parent)
        self.__init_sizer()
        
    def __create_dir_tree(self):
        """Create the directory tree."""
        self.dirPicker = DirectoryList(
                self.selectionArea,
                wxID_SELECTIONAREADIRPICKER,
                u'dirPicker',
                main.prefs.get('showHiddenDirs')
            )
        self.dirPicker.bind()

    def __on_recursive_checkbox(self, event):
        if self.walkIt.GetValue():
            self.foldersOn.Enable(False)
            self.filesOn.Enable(False)
            self.walkDepth.Enable(True)
            self.staticText2.Enable(True)
        else:
            self.foldersOn.Enable(True)
            self.filesOn.Enable(True)
            self.walkDepth.Enable(False)
            self.staticText2.Enable(False)
        if event:
            self._refresh_items(event)

    def __regex_options(self, event):
        """Enable display regexp options."""
        if self.filterByRE.GetValue():
            self.ignoreCase.Enable(True)
            self.useLocale.Enable(True)
        else:
            self.ignoreCase.Enable(False)
            self.useLocale.Enable(False)
        if event:
            self._refresh_items(event)

    def _refresh_items(self, event):
        self.Core.refresh(True)

    def _on_filter_sel(self, event):
        """Set common searches."""
        filter = self.FilterSel
        if self.get_in_searches(filter.GetStringSelection()):
            checkboxes = (self.filterByRE, self.ignoreCase, self.useLocale)
            for chckbx in checkboxes:
                chckbx.SetValue(True)
                chckbx.Enable(True)
        else:
            filter.SetLabel(u'')
            filter.SetValue(u'')
        self._refresh_items(event)

    def get_in_searches(self, key=False):
        """
        If a key is pecified, get the requested value,
        otherwise return all keys
        """
        if key != False:
            value = False
            for search in self.Core.CommonSearches:
                if search[0] == key:
                    value = search[1]
                    break
            return value
        else:
            keys = []
            for search in self.Core.CommonSearches:
                keys.append(search[0])
            return keys

    def on_config_load(self,):
        """Adjustments after loading config."""
        self.__regex_options(False)

    def remove_item_by_name(self, displayedName):
        ID = self.ItemList.FindItem(0,displayedName)
        item = wx.ListItem()
        item.SetId(ID)
        item.SetBackgroundColour(main.prefs.get(u'backgroundColor'))
        item.SetTextColour(main.prefs.get(u'textColor'))
        self.Panel.ItemList.SetItem(item)
    
    def reset_dirpicker_on_config_load(self):
        """Used when a config is loaded to ensure dirpicker behaves correctly."""
        if main.prefs.get('useDirTree') and \
        self.dirPicker.GetPath() != self.path.GetValue():
            self.dirPicker.unbind()
            self.dirPicker.SetPath(self.path.GetValue())
            self.dirPicker.bind()
        self._refresh_items(True)

    def set_tree(self):
        """Hide or show directory tree."""
        if main.prefs.get(u'useDirTree'):
            self.__create_dir_tree()
            self.dirPicker.SetPath(self.path.GetValue())
        else:
            self.selectionArea.Unsplit(self.dirPicker)
            self.dirPicker.Destroy()
        self.__init_splitter()

    def refresh_dirpicker(self):
        self.dirPicker.refresh_tree()

    def browse_for_path(self, event):
        """Get and set path."""
        dlg = wx.DirDialog(self,_(u"Choose a directory:"),
            style=wx.DD_DEFAULT_STYLE)
        dlg.SetPath(self.path.GetValue())
        try:
            if dlg.ShowModal() == wx.ID_OK:
                dir = dlg.GetPath()
                self.path.SetValue(dir)
                self.Core.set_path(event)
        finally: dlg.Destroy()


    def set_path(self, event):
        """Set the picker path."""
        if main.prefs.get(u'useDirTree'):
            # keep a record of the original path
            path = self.path.GetValue()
            # need to temporarily unbind to avoid showing picker twice
            self.dirPicker.Bind(wx.EVT_TREE_SEL_CHANGED, utils.dev_null)
            try:
                self.dirPicker.SetPath(path)
            except AttributeError:
                pass
            # OK bind again
            self.dirPicker.Bind(wx.EVT_TREE_SEL_CHANGED, self.dirPicker.dir_change)
            # if tree won't display original path, force it
            if self.dirPicker.GetPath() != path:
                self.path.SetValue(path)


    def select_all(self, event):
        """Add all items to renaming list."""
        # clear list
        self.Core.clear_joined_items()
        for i in range(self.ItemList.GetItemCount()):
            # add to list
            self.Core.joinedItems.append(self.ItemList._get_item_info(i))
            # show selected in picker
            item = wx.ListItem()
            item.SetId(i)
            #item.SetState(wx.LIST_STATE_SELECTED|wx.LIST_STATE_FOCUSED)
            item.SetBackgroundColour(main.prefs.get(u'highlightColor'))
            item.SetTextColour(main.prefs.get(u'highlightTextColor'))
            self.ItemList.SetItem(item)
        # enable buttons
        self.ItemList.Refresh()
        self.selectNone.Enable(True)
        main.menuPicker.getNoneMenu.Enable(True)
        self.selectAll.Enable(False)
        main.menuPicker.getAllMenu.Enable(False)
        main.currentItem = None
        main.show_preview(event)


    def select_none(self, event):
        """Remove all items from renaming list."""
        total_items = self.ItemList.GetItemCount()
        # clear list
        self.Core.clear_joined_items()
        # show deselected in picker
        for i in range(total_items):
            item = wx.ListItem()
            item.SetId(i)
            item.SetBackgroundColour(main.prefs.get(u'backgroundColor'))
            item.SetTextColour(main.prefs.get(u'textColor'))
            self.ItemList.SetItem(item)
        # enable buttons
        self.selectAll.Enable(True)
        main.menuPicker.getAllMenu.Enable(True)
        self.selectNone.Enable(False)
        main.menuPicker.getNoneMenu.Enable(False)
        main.currentItem = None
        main.errors.clear()
        main.set_status_msg(_(u"All items were deselected"), 'eyes')
        main.show_preview(event)

    def enable_buttons(self):
        """Enable buttons."""
        total_items = self.ItemList.GetItemCount()
        if self.Core.joinedItems != []:
            self.selectNone.Enable(True)
            main.menuPicker.getNoneMenu.Enable(False)
            if len(self.Core.joinedItems) == total_items:
                self.selectAll.Enable(False)
                main.menuPicker.getAllMenu.Enable(False)
            else:
                self.selectAll.Enable(True)
                main.menuPicker.getAllMenu.Enable(True)
        else:
            self.selectAll.Enable(True)
            main.menuPicker.getAllMenu.Enable(True)
            self.selectNone.Enable(False)
            main.menuPicker.getNoneMenu.Enable(False)


    def walk_from_menu(self):
        """When setting walk checkbox from app menu."""
        if self.walkIt.GetValue() == False:
            self.walkIt.SetValue(True)
        else:
            self.walkIt.SetValue(False)
        self.__on_recursive_checkbox(True)

