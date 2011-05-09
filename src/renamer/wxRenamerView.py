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

"""
The renamer panel, it allows displaying and controlling all operation panels.
"""

import re

import app
import operations
import utils
import wx

[wxID_, wxID_APPLYEXTENSION, wxID_APPLYNAME,
	wxID_AVAILABLEOPERATIONS, wxID_DELETEOPERATION,
	wxID_ENABLEOPERATION, wxID_MOVEDOWN, wxID_MOVEUP,
	wxID_STATICTEXT1, wxID_STATICTEXT2,
	wxID_STATICTEXT3, wxID_STATICTEXT4,
	wxID_USEDOPERATIONS, wxID_STATICTEXT5,
	wxID_MENUUP, wxID_MENUDOWN, wxID_DELETEOPERATIONS,
	wxID_MENURESET, wxID_MENUSETSTATUS,
	wxID_MENUDISABLE, wxID_MENUAPPLYNAME,
	wxID_MENUAPPLYEXTENSION, wxID_MENUDESTROY,
	wxID_MENUDESTROYALL, wxID_RESETOPERATIONBUTTON,
] = [wx.NewId() for __init_ctrls in range(25)]


BackgroundClr = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
HighlightClr = wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT)
HighlightTxtClr = wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
TxtClr = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWTEXT)

class OperationDropTarget(wx.TextDropTarget):
    def __init__(self, object):
        wx.TextDropTarget.__init__(self)
        self.object = object
        self.prnt = object.GetParent()
        self.itemCount = 0

    def __reset_highlight(self, last=True):
        """set all items to deselected"""
        for pos in range(self.itemCount):
            item = wx.ListItem()
            item.SetId(pos)
            item.SetBackgroundColour(BackgroundClr)
            item.SetTextColour(TxtClr)
            self.prnt.usedOperations.SetItem(item)
            if not last:
                self.object.SetItemState(pos, 0, wx.LIST_STATE_SELECTED)

    # overloads builtin method
    def HitTest(self, x, y):
        return self.object.HitTest(wx.Point(x, y))

    # overloads builtin method
    def OnLeave(self):
        self.itemCount = self.object.GetItemCount()
        self.__reset_highlight()
        self.prnt.usedOperations.Refresh()
        if self.curSelected is not None:
            self.object.Select(self.curSelected)

    # overloads builtin method
    def OnEnter(self, x, y, d):
        self.itemCount = self.prnt.usedOperations.GetItemCount()
        self.curSelected = self.prnt.get_current_operation_numb()
        return d

    # overloads builtin method
    def OnDragOver(self, x, y, d):
        #print "OnDragOver: %d, %d, %d" % (x, y, d)
        pos = self.HitTest(x, y)[0]
        if pos != -1:
            self.__reset_highlight(False)
            item = wx.ListItem()
            item.SetId(pos)
            item.SetBackgroundColour(HighlightClr)
            item.SetTextColour(HighlightTxtClr)
            item.SetState(wx.LIST_STATE_FOCUSED)
            self.prnt.usedOperations.SetItem(item)
            self.prnt.usedOperations.Refresh()
        return d

    # overloads builtin method
    def OnDropText(self, x, y, data):
        pos = self.HitTest(x, y)[0]
        if pos < 0:
            pos = self.itemCount - 1
        if ':' in data:
            n = int(re.search('\d*', data).group(0))
            moveBy = (pos - n) + 1
            self.prnt.move_operations(moveBy, n-1)
        else:
            self.prnt.stack_operation(data, pos)
        self.__reset_highlight()


class UsedOperations(wx.ListCtrl):
    """
    Used operations list
    """
    def __init__(self, id, name, parent, w, scrollBarSize):
        wx.ListCtrl.__init__(self, parent=parent, id=id, size=wx.Size(w, -1),
							 style=wx.LC_REPORT | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL, name=name)
        self.InsertColumn(0, '', format=wx.LIST_FORMAT_LEFT, width=w-scrollBarSize)


class IntroTextPanel(wx.Panel):
    """
    Show intro text, set app size
    """
    def __init__(self, prnt, id):
        wx.Panel.__init__(self, id=id, name=u'IntroTextPanel',
						  parent=prnt, style=wx.TAB_TRAVERSAL)

        # create info text of available operations
        # Find largest panel, use it to set this panel size
        txt = ''
        txtSize = (0, 0)
        for i in range(prnt.availableOperations.GetItemCount()):
            op = prnt.availableOperations.GetItemText(i)
            txt += "%s  :  %s\n\n" % (op, operations.defs[op][1])

            # create temporary instance of panel to get size
            op = operations.defs[op][0]
            opPanel = getattr(operations, op).OpPanel(prnt, main)
            size = opPanel.GetSizeTuple()
            if size > txtSize:
                txtSize = size
            opPanel.Destroy()

        fontParams = app.fontParams
        fontSize = fontParams['size']
        fontFamily = fontParams['family']
        fontStyle = fontParams['style']

        # adjust vertical spacing for top bar
        gap = prnt.moveDown.GetSizeTuple()[1] + 24

        self.staticText1 = wx.StaticText(id=-1,
										 label=_(u"You don't have any operations defined."),
										 name='staticText1', parent=self, style=wx.ALIGN_LEFT,
										 size=wx.Size(txtSize[0], -1))
        self.staticText1.SetFont(wx.Font(fontSize + 3, fontFamily, fontStyle, wx.BOLD))

        label = _("Double-click or drag && drop an operation in the 'Available' box to add one.")
        label += _("\nYou may then drag && drop used operations to reorder them.")
        self.staticText2 = wx.StaticText(id=-1, label=label,
										 name='staticText2', parent=self, style=wx.ALIGN_LEFT,
										 size=wx.Size(txtSize[0], -1))
        self.staticText2.SetFont(wx.Font(fontSize, fontFamily, fontStyle, wx.BOLD))

        self.staticText3 = wx.StaticText(id=-1,
										 label=txt, name='staticText3', parent=self,
										 style=wx.ALIGN_LEFT, size=wx.Size(txtSize[0], -1))

        # add to sizer
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.staticText1, 0, wx.BOTTOM, 5)
        mainSizer.Add(self.staticText2, 0, wx.BOTTOM, 15)
        mainSizer.Add(self.staticText3, 0)
        self.SetSizer(mainSizer)

        # set size based on calculations above
        self.SetMinSize(wx.Size(txtSize[0], txtSize[1] + gap))



class Panel(wx.Panel):
    def __init_sizers(self):
        mainSizer = self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        leftSizer = wx.BoxSizer(wx.VERTICAL)
        leftSizer.AddWindow(self.staticText1, 0, )
        leftSizer.AddWindow(self.availableOperations, 0, wx.BOTTOM, 5)
        leftSizer.AddWindow(self.staticText2, 0, wx.TOP, 5)
        leftSizer.AddWindow(self.usedOperations, 1)
        mainSizer.AddSizer(leftSizer, 0, wx.EXPAND | wx.ALL, 5)

        rightSizer = self.rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightTopSizer = self.rightTopSizer = wx.BoxSizer(wx.HORIZONTAL)
        rightTopSizer.AddWindow(self.staticText3, 0, wx.ALIGN_CENTRE | wx.LEFT, 5)
        rightTopSizer.AddWindow(self.moveDown, 0, wx.ALIGN_CENTRE | wx.LEFT, 3)
        rightTopSizer.AddWindow(self.moveUp, 0, wx.ALIGN_CENTRE | wx.RIGHT, 25)
        rightTopSizer.AddSpacer((-1, 1), 1)
        rightTopSizer.AddWindow(self.staticText4, 0, wx.ALIGN_CENTRE | wx.RIGHT, 5)
        rightTopSizer.AddWindow(self.applyName, 0, wx.ALIGN_CENTRE | wx.RIGHT, 3)
        rightTopSizer.AddWindow(self.applyExtension, 0, wx.ALIGN_CENTRE | wx.RIGHT, 15)
        rightTopSizer.AddSpacer((-1, 1), 5)
        rightTopSizer.AddWindow(self.enableOperation, 0, wx.ALIGN_CENTRE | wx.RIGHT, 5)
        rightTopSizer.AddWindow(self.resetOperationButton, 0, wx.ALIGN_CENTRE | wx.RIGHT, 10)
        rightTopSizer.AddWindow(self.deleteOperations, 0, wx.ALIGN_CENTRE | wx.RIGHT, 5)
        rightTopSizer.AddSpacer((-1, 1), 5)
        rightSizer.AddSizer(rightTopSizer, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 3)
        rightTopSizer.AddSpacer((1, 10), 0)
        rightSizer.AddWindow(self.staticText5, 0, flag=wx.LEFT, border=20)

        mainSizer.AddSizer(rightSizer, 1, wx.EXPAND)
        self.SetSizerAndFit(mainSizer)

    def __init_menu(self, parent, n):
        """
        The used operations' right click menu
        """
        # 'apply to' sub menu
        parent.applyTo = applyTo = wx.Menu()
        applyTo.name = wx.MenuItem(applyTo, wxID_MENUAPPLYNAME,
								   _(u"Name"), kind=wx.ITEM_CHECK)
        applyTo.extension = wx.MenuItem(applyTo, wxID_MENUAPPLYEXTENSION,
										_(u"Extension"), kind=wx.ITEM_CHECK)

        applyTo.AppendItem(applyTo.name)
        applyTo.AppendItem(applyTo.extension)

        self.Bind(wx.EVT_MENU, self.__set_operations_apply_menu,
				  id=wxID_MENUAPPLYNAME)
        self.Bind(wx.EVT_MENU, self.__set_operations_apply_menu,
				  id=wxID_MENUAPPLYEXTENSION)

        opPanel = self.Core.operations[n]

        if opPanel.params['applyName']:
            applyTo.name.Check(True)
        if opPanel.params['applyExtension']:
            applyTo.extension.Check(True)

        # main menu
        parent.up = wx.MenuItem(parent, wxID_MENUUP, _(u"Move up"))
        parent.up.SetBitmap(wx.Bitmap(utils.icon_path(u'up.png'),
							wx.BITMAP_TYPE_PNG))

        parent.down = wx.MenuItem(parent, wxID_MENUDOWN, _(u"Move down"))
        parent.down.SetBitmap(wx.Bitmap(utils.icon_path(u'down.png'),
							  wx.BITMAP_TYPE_PNG))

        if opPanel.IsEnabled():
            txt = _(u"Disable")
            ico = 'disable'
        else:
            txt = _(u"Enable")
            ico = 'enable'
        parent.disable = wx.MenuItem(parent, wxID_MENUDISABLE, txt)
        parent.disable.SetBitmap(wx.Bitmap(utils.icon_path(u"%s.png" % ico),
								 wx.BITMAP_TYPE_PNG))

        parent.reset = wx.MenuItem(parent, wxID_MENURESET, _(u"Reset"))
        parent.reset.SetBitmap(wx.Bitmap(utils.icon_path(u'reset_op.png'),
							   wx.BITMAP_TYPE_PNG))

        parent.destroy = wx.MenuItem(parent, wxID_MENUDESTROY, _(u"Destroy"))
        parent.destroy.SetBitmap(wx.Bitmap(utils.icon_path(u'errors.ico'),
								 wx.BITMAP_TYPE_ICO))

        parent.destroyAll = wx.MenuItem(parent, wxID_MENUDESTROYALL, _(u"Destroy All"))
        parent.destroyAll.SetBitmap(wx.Bitmap(utils.icon_path(u'nuke.png'),
									wx.BITMAP_TYPE_PNG))

        parent.setStatus = wx.MenuItem(parent, wxID_MENUSETSTATUS, _(u"Enable/Disable"))
        parent.setStatus.SetBitmap(wx.Bitmap(utils.icon_path(u're.ico'),
								   wx.BITMAP_TYPE_ICO))

        parent.AppendItem(parent.up)
        parent.AppendItem(parent.down)
        if _(u"directory") not in self.usedOperations.GetItemText(n):
            parent.applyToMenu = wx.MenuItem(parent, -1, _(u"Apply to"),
											 subMenu=applyTo)
            parent.AppendItem(parent.applyToMenu)
        parent.AppendItem(parent.disable)
        parent.AppendItem(parent.reset)
        parent.AppendItem(parent.destroy)
        parent.AppendItem(parent.destroyAll)

        self.Bind(wx.EVT_MENU, self.__move_up_button,
				  id=wxID_MENUUP)
        self.Bind(wx.EVT_MENU, self.__move_down_button,
				  id=wxID_MENUDOWN)
        self.Bind(wx.EVT_MENU, self.__operation_toggle_btn,
				  id=wxID_MENUDISABLE)
        self.Bind(wx.EVT_MENU, self.__reset_operation,
				  id=wxID_MENURESET)
        self.Bind(wx.EVT_MENU, self.delete_operation,
				  id=wxID_MENUDESTROY)
        self.Bind(wx.EVT_MENU, self.__destroy_all_gui_operations,
				  id=wxID_MENUDESTROYALL)


    def __init_ctrls(self, prnt):
        wx.Panel.__init__(self, id=wxID_, name=u'mainPanel',
						  parent=prnt, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL)

        self.staticText1 = wx.StaticText(id=wxID_STATICTEXT1,
										 label=_(u"Available:"), name='staticText1', parent=self,
										 style=0)

        self.availableOperations = wx.ListCtrl(id=wxID_AVAILABLEOPERATIONS,
											   name=u'availableOperations', parent=self,
											   style=wx.LC_REPORT | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL)
        self.availableOperations.Bind(wx.EVT_LIST_ITEM_ACTIVATED,
									  self.stack_operation, id=wxID_AVAILABLEOPERATIONS)

        self.availableOperations.InsertColumn(0, '', format=wx.LIST_FORMAT_LEFT, width=-1)

        # add operations to list
        i = 0
        for op in sorted(operations.defs.keys()):
            self.availableOperations.InsertStringItem(i, op)
            i += 1

        # set vertical size
        h = self.availableOperations.GetItemRect(0)[-1]
        ops = self.availableOperations.GetItemCount()
        if wx.Platform == '__WXMSW__':
            h = (h * ops) + 6
        else:
            h = h * ops
        
        # set horizontal size
        longest = operations.get_longest_name_length()
        w = app.fontParams['size'] * longest

        scrollBarSize = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
        Size = (w, h)
        
        self.availableOperations.SetMinSize(Size)
        self.availableOperations.SetColumnWidth(0, w-scrollBarSize)

        self.usedOperations = UsedOperations(wxID_USEDOPERATIONS,
											 u'usedOperations', self, w, scrollBarSize)
        self.usedOperations.Bind(wx.EVT_LIST_ITEM_SELECTED,
								 self.__used_operations_listbox, id=wxID_USEDOPERATIONS)

        self.staticText2 = wx.StaticText(id=wxID_STATICTEXT2,
										 label=_(u"Used:"), name='staticText2', parent=self,
										 style=0)

        self.moveDown = wx.BitmapButton(bitmap=wx.Bitmap(utils.icon_path(u'down.png'),
										wx.BITMAP_TYPE_PNG), id=wxID_MOVEDOWN, name=u'moveDown',
										parent=self, style=wx.BU_AUTODRAW)
        self.moveDown.SetToolTipString(_(u"Move current operation down by 1"))
        self.moveDown.Bind(wx.EVT_BUTTON, self.__move_down_button,
						   id=wxID_MOVEDOWN)

        self.moveUp = wx.BitmapButton(bitmap=wx.Bitmap(utils.icon_path(u'up.png'),
									  wx.BITMAP_TYPE_PNG), id=wxID_MOVEUP, name=u'moveUp',
									  parent=self, style=wx.BU_AUTODRAW)
        self.moveUp.SetToolTipString(_(u"Move current operation up by 1"))
        self.moveUp.Bind(wx.EVT_BUTTON, self.__move_up_button,
						 id=wxID_MOVEUP)

        self.enableOperation = wx.ToggleButton(id=wxID_ENABLEOPERATION,
											   label=_(u"Disable"), name=u'enableOperation', parent=self,
											   style=wx.BU_EXACTFIT)
        self.enableOperation.SetToolTipString(_(u"Enable or Disable current operation"))
        self.enableOperation.SetValue(False)
        self.enableOperation.Bind(wx.EVT_TOGGLEBUTTON,
								  self.__operation_toggle_btn, id=wxID_ENABLEOPERATION)

        self.deleteOperations = wx.Choice(choices=[_(u"Destroy"), _(u"Destroy All")],
										  id=wxID_DELETEOPERATIONS, name=u'actions', parent=self)
        self.deleteOperations.SetSelection(0)
        self.deleteOperations.SetToolTipString(_(u"Do Stuff"))
        self.deleteOperations.Bind(wx.EVT_CHOICE, self.__actions_choice, id=wxID_DELETEOPERATIONS)

        self.resetOperationButton = wx.Button(id=wxID_RESETOPERATIONBUTTON,
											  label=_(u"Reset"), name=u'resetOperationButton', parent=self,
											  style=wx.BU_EXACTFIT)
        self.resetOperationButton.SetToolTipString(_(u"Reset the current operation"))
        self.resetOperationButton.Bind(wx.EVT_BUTTON, self.__reset_operation,
									   id=wxID_RESETOPERATIONBUTTON)

        self.staticText3 = wx.StaticText(id=wxID_STATICTEXT3,
										 label=_(u"Order:"), name='staticText3', parent=self,
										 style=0)

        self.applyExtension = wx.CheckBox(id=wxID_APPLYEXTENSION,
										  label=_(u"extension"), name=u'applyExtension', parent=self,
										  style=0)
        self.applyExtension.SetValue(False)
        self.applyExtension.Bind(wx.EVT_CHECKBOX, self.__set_operations_apply,
								 id=wxID_APPLYEXTENSION)

        self.applyName = wx.CheckBox(id=wxID_APPLYNAME,
									 label=_(u"name"), name='applyName', parent=self, style=0)
        self.applyName.SetValue(True)
        self.applyName.Bind(wx.EVT_CHECKBOX, self.__set_operations_apply,
							id=wxID_APPLYNAME)

        self.staticText4 = wx.StaticText(id=wxID_STATICTEXT4,
										 label=_(u"Apply to:"), name='staticText4', parent=self,
										 style=0)

        self.staticText5 = IntroTextPanel(self, wxID_STATICTEXT5)

        dt = OperationDropTarget(self.usedOperations)
        self.usedOperations.SetDropTarget(dt)

        wx.EVT_LIST_BEGIN_DRAG(self.availableOperations, self.availableOperations.GetId(),
							   self.__available_drag_init)
        wx.EVT_LIST_BEGIN_DRAG(self.usedOperations, self.usedOperations.GetId(),
							   self.__used_drag_init)


    def __init__(self, Core, parent, main_window):
        global main
        main = main_window
        self.Core = Core
        self.__init_ctrls(parent)
        self.__init_sizers()
        self.__set_button_state()
        # capture right clicks in several areas
        for area in (self, self.usedOperations):
            # for wxMSW
            area.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.__on_right_click)
            # for wxGTK
            area.Bind(wx.EVT_RIGHT_UP, self.__on_right_click)

    def __reassign_numbers(self):
        for i in range(self.usedOperations.GetItemCount()):
            original = self.usedOperations.GetItemText(i)
            self.usedOperations.SetItemText(i, str(i + 1) + ":" + original.split(":")[1])

    def __on_right_click(self, event):
        """
        Popup the menu
        """
        self.operationsMenu = wx.Menu()
        n = self.get_current_operation_numb()
        if n != None:
            self.__init_menu(self.operationsMenu, n)
            self.PopupMenu(self.operationsMenu)

    def __current_operation_panel(self):
        """
        currently selected operation panel
        """
        n = self.get_current_operation_numb()
        if n != None:
            return self.Core.operations[n]

    def __available_drag_init(self, event):
        """
        Start dragging from available operations, for adding
        """
        text = self.availableOperations.GetItemText(event.GetIndex())
        tdo = wx.PyTextDataObject(text)
        tds = wx.DropSource(self.availableOperations)
        tds.SetData(tdo)
        tds.DoDragDrop(True)

    def __used_drag_init(self, event):
        """
        Start dragging from used operations, for re-aranging
        """
        text = self.usedOperations.GetItemText(event.GetIndex())
        tdo = wx.PyTextDataObject(text)
        tds = wx.DropSource(self.usedOperations)
        tds.SetData(tdo)
        tds.DoDragDrop(True)

    def __add_operation_to_sizer(self, opPanel):
        self.rightSizer.Detach(self.staticText5)
        self.staticText5.Show(False)
        self.rightSizer.Add(opPanel, 1, wx.EXPAND | wx.RIGHT, 5)
        self.mainSizer.Layout()

    def __add_operation_to_list(self, pos, opName):
        self.usedOperations.InsertStringItem(pos, unicode(pos + 1) + u": " + opName)

    def __set_operations_apply_menu(self, event):
        """
        Set 'apply to' from menu.
        """
        id = event.GetId()
        if id == wxID_MENUAPPLYNAME:
            checked = self.operationsMenu.applyTo.name.IsChecked()
            self.applyName.SetValue(checked)
        else:
            checked = self.operationsMenu.applyTo.extension.IsChecked()
            self.applyExtension.SetValue(checked)
        self.__set_operations_apply(event)

    def __set_operations_apply(self, event):
        """
        set to which part of name operation applies to
        """
        operation = self.__current_operation_panel()
        if operation is not False:
            operation.params['applyName'] = self.applyName.GetValue()
            operation.params['applyExtension'] = self.applyExtension.GetValue()
            main.show_preview(event)

    def __show_apply_checkboxes(self, show):
        """Enable or disable apply_to checkboxes."""
        chkbx = (self.applyName, self.applyExtension)
        if show:
            for box in chkbx:
                box.Enable(True)
            self.applyName.SetValue(True)
            self.applyExtension.SetValue(False)
        else:
            for box in chkbx:
                box.SetValue(False)
                box.Enable(False)

    def __set_button_state(self):
        """Enable/disable delete and enable buttons."""
        opButtons = (self.enableOperation, self.resetOperationButton,
					 self.deleteOperations,
					 self.moveUp, self.moveDown)
        if len(self.Core.operations) < 1:
            for i in opButtons:
                i.Enable(False)
            for i in (self.applyName, self.applyExtension):
                i.Enable(False)
        else:
            for i in opButtons:
                i.Enable(True)

    def __show_operation(self, n):
        """Show a specific operation."""
        # need to hide other operations first
        for opPanel in self.Core.operations:
            opPanel.Show(False)
            self.rightSizer.Detach(opPanel)

        # now show selected one
        opPanel = self.Core.operations[n]
        opPanel.Show(True)
        self.__add_operation_to_sizer(opPanel)

        if not opPanel.params['applyPathOnly']:
            # show if name and/or extension is operated on:
            self.applyName.SetValue(opPanel.params['applyName'])
            self.applyExtension.SetValue(opPanel.params['applyExtension'])

            self.applyName.Enable(True)
            self.applyExtension.Enable(True)
        else:
            self.__show_apply_checkboxes(False)

        # show operation button as enabled/disabled
        if opPanel.IsEnabled():
            self.enableOperation.SetLabel(_(u"Disable"))
            self.enableOperation.SetValue(False)
        else:
            self.enableOperation.SetLabel(_(u"Enable"))
            self.enableOperation.SetValue(True)
        self.mainSizer.Layout()


    def __used_operations_listbox(self, event):
        """show operation from box."""
        n = self.get_current_operation_numb()
        if n != None:
            self.__show_operation(n)

    def __operation_toggle_btn(self, event):
        """Enable or disable the currently selected operation."""
        opPanel = self.__current_operation_panel()
        if opPanel != None:
            if opPanel is not False:
                if opPanel.IsEnabled():
                    opPanel.Enable(False)
                    self.enableOperation.SetLabel(_(u"Enable"))
                else:
                    opPanel.Enable(True)
                    self.enableOperation.SetLabel(_(u"Disable"))
                self.mainSizer.Layout()
                main.show_preview(event)

    def __reset_operation(self, event):
        """Destroy, then recreate operation (reset)."""
        n = self.get_current_operation_numb()
        if n != None:
            text = self.usedOperations.GetItemText(n)
            text = re.search("(?<=: ).+$", text)
            op = text.group()
            dlg = wx.MessageDialog(self, _("Really reset this '%s' operation?") % op,
								   _("Are You Sure?"), wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)
            if dlg.ShowModal() == wx.ID_YES:
                # delete operation:
                self.Core.delete_operation(n)

                # create new of same type/position
                opPanel = self.create_operation(n, op)

                # add it to the window properly
                self.__add_operation_to_sizer(opPanel)
                main.show_preview(event)

    def __move_down_button(self, event):
        self.move_operations( + 1)

    def __move_up_button(self, event):
        self.move_operations(-1)

    def __destroy_all_gui_operations(self, event):
        """Destroy all operations from GUI."""
        if self.Core.operations:
            msg = _("Really destroy all operations?")
            title = _("Are You Sure?")
            if utils.make_yesno_dlg(msg, title):
                self.destroy_all_operations()
                main.show_preview(event)

    def __actions_choice(self, event):
        """Execute correct function based on user selected action."""
        selected = self.deleteOperations.GetSelection()
        result = {0: self.delete_operation,
			1: self.__destroy_all_gui_operations,
		}[selected](event)
        self.deleteOperations.SetSelection(0)
    
    def stack_operation(self, event, pos=-1, params={}):
        if type(event) == type(u''):
            op = event
            #event = False
        else:
            op = event.GetLabel()

        # adding operation
        if pos == -1:
            pos = self.usedOperations.GetItemCount()
        # loading operation from config
        elif type(pos) == type(u' '):
            pos = int(pos)
        # inserting operation
        else:
            pos += 1

        # add requested operation
        self.__add_operation_to_list(pos, op)
        opPanel = self.create_operation(pos, op, params)
        self.__reassign_numbers()

        # add window to sizer:
        self.__add_operation_to_sizer(opPanel)

        self.usedOperations.Select(pos)
        self.__set_button_state()
        main.show_preview(event)

    def create_operation(self, n, op, params={}):
        opPanel = self.Core.create_operation(n, op, params)
        return opPanel

    def move_operations(self, To, n=None):
        """
        Change the placement of an operation, adjusting others as needed.
        """
        if n == None:
            n = self.get_current_operation_numb()
        if n != None:
            moveTo = n + To
            if self.usedOperations.GetItemCount() > moveTo and moveTo > -1:
                oldText = self.usedOperations.GetItemText(n)

                self.usedOperations.DeleteItem(n)
                self.usedOperations.InsertStringItem(moveTo, oldText)
                self.__reassign_numbers()
                self.Core.move_operations(n, moveTo)
                self.usedOperations.Select(moveTo)
            main.show_preview(True)

    def get_current_operation_numb(self):
        """
        currently selected operation number
        """
        usedOps = self.usedOperations
        if usedOps.GetSelectedItemCount() > 0:
            return usedOps.GetNextItem(-1, state=wx.LIST_STATE_SELECTED)

    def delete_operation(self, event):
        """
        Delete an operation, then reasign numbers to remaining ones.
        """
        n = self.get_current_operation_numb()
        if n != None:
            type = self.usedOperations.GetItemText(n)
            type = re.sub("\d{1,}: ", '', type)

            dlg = wx.MessageDialog(self, _("Really destroy this '%s' operation?") % type,
								   _("Are You Sure?"), wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)
            if dlg.ShowModal() == wx.ID_YES:
                # delete operation:
                self.usedOperations.DeleteItem(n)
                self.Core.delete_operation(n)
                self.__reassign_numbers()

                # select another operation, if present
                if len(self.Core.operations) > 0:
                    # there is a preceding operation
                    if n-1 > -1:
                        n = n-1
                    self.__show_operation(n)
                    self.usedOperations.Select(n)
                # otherwise show text
                else:
                    self.staticText5.Show(True)
                self.__set_button_state()
                main.show_preview(event)

    def destroy_all_operations(self):
        """Destroy all operations in stack."""
        self.Core.destroy_all_operations()
        self.usedOperations.DeleteAllItems()
        self.staticText5.Show(True)
        self.__set_button_state()

