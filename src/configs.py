# -*- coding: utf-8 -*-

# Handles writing and loading XML configuration files

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
Handle loading and saving configuration XML files.
"""

import wx
import codecs
import time
import re
from os import path
from xml.dom import minidom
from xml.sax.saxutils import escape
from xml.sax.saxutils import unescape


import utils
import operations


def save(main):
    """Get values, write configuration file."""
    # save dialog
    dlg = wx.FileDialog(None, message=_(u"Save configuration as ..."),
          defaultDir=utils.get_user_path(u'configs'), defaultFile=u'.cfg',
          wildcard=_(u"Configuration file (*.cfg)")+u'|*.cfg',
          style=wx.SAVE|wx.OVERWRITE_PROMPT
          )
    # write file
    if dlg.ShowModal() == wx.ID_OK:
        cfgFilePath = dlg.GetPath()
        cfgFileExt = path.splitext(cfgFilePath)[1]
        if cfgFileExt != '.cfg':
            cfgFilePath = cfgFilePath + '.cfg'
        # create and write the file
        utils.write_file(cfgFilePath, SaveConfig(main).cfgFile)
    dlg.Destroy()


def load(main, configFilePath=False):
    """Get config file path from dialog and apply settings."""
    if configFilePath:
        LoadConfig(main, configFilePath)
    else:
        dlg = wx.FileDialog(None,
          message=_(u"Load a configuration file"),
          defaultDir=utils.get_user_path('configs'), defaultFile=u'',
          wildcard=_(u"Configuration file (*.cfg)")+u'|*.cfg',
          style=wx.OPEN
          )
        if dlg.ShowModal() == wx.ID_OK:
            LoadConfig(main, dlg.GetPath())
        dlg.Destroy()


class SaveConfig():
    """
    Save the current configuration.
    Instanciating the class saves the configuration.
    """
    def __init__(self, mainWindow):
        global main
        main = mainWindow
        self.cfgFile = self.__create_file()

    def __get_child_values(self, child):
        """Get correct values depending on child type."""
        value = None
        if isinstance(child, wx.CheckBox) or isinstance(child, wx.RadioButton):
            value = int(child.GetValue())
        elif isinstance(child, wx.TextCtrl) or isinstance(child, wx.SpinCtrl):
            value = child.GetValue()
        elif isinstance(child, wx.ComboBox):
            value = child.GetValue()
        elif isinstance(child, wx.Choice):
            value = child.GetSelection()
        if value is not None:
            if type(value) == type(u''):
                value = escape(value)
            widgetType = child.GetClassName()
            id = child.GetName()
            return id, widgetType, value

    def _all_child_params_to_xml(self, cfg, child, r):
        """
        Recursively get the complete path down hierachy to value.
        End result is a XML structure of values.
        """
        # panels & notebook get children
        if isinstance(child, wx.Notebook) or isinstance(child, wx.Panel):
            type = child.GetClassName()
            id = child.GetName()
            cfg += '\t\t\t'+r*'\t'+u'<%s id="%s">\n'%(type,id)
            for child in child.GetChildren():
                try:
                    cfg = self._all_child_params_to_xml(cfg, child, r+1)
                except TypeError:
                    pass
            cfg += '\t\t\t'+r*'\t'+u"</%s>\n"%type
            return cfg
        # others get values
        else:
            try:
                id, widgetType, value = self.__get_child_values(child)
            except TypeError:
                pass
            else:
                cfg += '\t\t\t'+r*'\t'+u'<value id="%s" type="%s">%s</value>\n'\
                      %(id, widgetType, value)
            return cfg

    def _renaming_ops_to_xml(self):
        """
        Convert all renaming operations to XML, including parameters and
        widget values.
        """
        cfg = ''
        operationList = main.renamer.view.usedOperations
        operationStack = main.renamer.operations

        for i in range(operationList.GetItemCount()):
            type = operationList.GetItemText(i)
            type = re.sub("\d{1,}: ", '', type)
            type = operations.defs[type][0]
            operation = operationStack[i]
            cfg += u'\t\t<operation id="%s" type="%s">\n'%(i, type)
            cfg += u'\t\t\t<parameters>\n'
            for k in operation.params.keys():
                v = operation.params[k]
                cfg += u'\t\t\t\t<%s>%s</%s>\n' % (k, v, k)
            cfg += '\t\t\t</parameters>\n'
            for child in operation.GetChildren():
                cfg = self._all_child_params_to_xml(cfg, child, 0)
            cfg += u'\t\t</operation>\n'
        return cfg

    def __create_file(self):
        """Create an XML configuration file."""
        datetime = utils.udate(main, '%Y-%m-%d %H:%M:%S', time.localtime())
        cfgFile = u'<?xml version="1.0" encoding="UTF-8"?>\n'
        cfgFile += u'<configuration application="Métamorphose-2" '+\
                   'version="%s" datetime="%s">\n'\
                   %(main.version, datetime)
        # get info for 'normal' notebook tabs
        pages = utils.get_notebook_page_names(main)
        for i in (0,2,3):
            # section header is page name
            cfgFile += u'\t<page id="%s" name="%s">\n'%(i,pages[i].GetName())
            for child in pages[i].GetChildren():
                try:
                    id,type,value = self.__get_child_values(child)
                except TypeError:
                    pass
                else:
                    cfgFile += u'\t\t<value id="%s" type="%s">%s</value>\n'\
                               %(id,type,value)
            cfgFile += u'\t</page>\n'

        # get renaming operations
        cfgFile += u'\t<page id="1" name="%s">\n'%pages[1].GetName()
        cfgFile += self._renaming_ops_to_xml()
        cfgFile += "\t</page>\n</configuration>\n"
        
        return cfgFile


class LoadConfig():
    """
    Load a configuration file and apply settings to the interface.
    This is done on class initialization.
    """
    def __init__(self, mainWindow, configFilePath):
        global main
        main = mainWindow
        self.__load_file(configFilePath)

    def __set_widget_value(self, id, type, value):
        """Set widget's value correctly depending on type."""
        if value == None:
            value = ''
        else:
            value = unescape(value)
        if type == 'wxCheckBox' or type == 'wxRadioButton' or type == 'wxSpinCtrl':
            id.SetValue(int(value))
        elif type == 'wxTextCtrl' or type == 'wxComboBox':
            id.SetValue(value)
        elif type == 'wxChoice':
            id.SetSelection(int(value))

    def __apply_values(self, parent, node):
        """
        Get widget values recursively through XML tree,
        apply setings to operation,
        """
        id = node.attributes['id'].value
        # value, apply
        if node.tagName == 'value':
            wtype = node.attributes['type'].value
            try:
                value = node.childNodes[0].nodeValue
            except IndexError:
                value = None
            try:
                widget = getattr(parent, id)
            except AttributeError:
                pass
            else:
                self.__set_widget_value(widget, wtype, value)
        # notebook, cycle through pages
        elif node.tagName == 'wxNotebook':
            notebook = getattr(parent, id)
            names = []
            for i in range(notebook.GetPageCount()):
                names.append(notebook.GetPage(i).GetName())
            for child in node.getElementsByTagName('wxPanel'):
                childname = child.attributes['id'].value
                if childname in names:
                    self.__apply_values(parent, child)
        # panel, cycle through panels and values
        elif node.tagName == 'wxPanel':
            #print parent, id
            parent = getattr(parent, id)
            for child in node.childNodes:
                if child.nodeType == 1:
                    self.__apply_values(parent, child)


    def __get_operation_params(self, op):
        """Get operation parameters from XML, return dict."""
        params = {}
        try:
            paramNode = op.getElementsByTagName('parameters')[0]
        except IndexError:
            utils.debug_print(main,
                u"warning : could not load all parameters for '%s' operation." % op.attributes['type'].value
            )
        else:
            for node in paramNode.childNodes:
                if node.nodeType == 1:
                     value = node.childNodes[0].nodeValue
                     if value == 'True': value = True
                     if value == 'False': value = False
                     params[node.nodeName] = value
        return params


    def __load_config_xml(self, config):
        pages = utils.get_notebook_page_names(main)
        configVersion = config.attributes['version'].value

        utils.debug_print(main, "config version : %s"%configVersion)

        for page in config.getElementsByTagName('page'):
            page_name = page.attributes['name'].value
            page_id = int(page.attributes['id'].value)

            # normal pages
            if page_name != 'mainPanel':
                utils.debug_print(main, "loading config page : %s"%page_name)

                for node in page.getElementsByTagName('value'):
                    id = node.attributes['id'].value
                    # make sure element exists before setting it
                    if hasattr(pages[page_id], id):
                        id = getattr(pages[page_id], id)
                    else:
                        continue
                    type = node.attributes['type'].value
                    try:
                        value = node.childNodes[0].nodeValue
                    except IndexError:
                        value = None
                    self.__set_widget_value(id, type, value)
                    # adjustments if needed
                    if hasattr(pages[page_id], 'on_config_load'):
                        pages[page_id].on_config_load()
            # main page
            else:
                utils.debug_print(main, "loading renamer config")
                # cleanup before loading
                main.renamer.view.destroy_all_operations()

                # load values
                for op in page.getElementsByTagName('operation'):
                    type = op.attributes['type'].value
                    type = operations.get_translated_name(type)
                    utils.debug_print(main, "loading operation type : %s"%type)

                    # make sure it's a valid type
                    if type == False:
                        continue
                    id = op.attributes['id'].value

                    # initialise object, passing parameters
                    params = self.__get_operation_params(op)
                    main.renamer.view.stack_operation(type, id, params)

                    # apply node values to widgets
                    operation = main.renamer.operations[int(id)]
                    for node in op.childNodes:
                        if node.nodeType == 1 and node.nodeName != "parameters":
                            self.__apply_values(operation, node)

                    # apply each operation's post load routine
                    if hasattr(operation, 'on_config_load'):
                        operation.on_config_load()


    def __load_file(self, configFilePath):
        """Read file and apply settings."""
        utils.debug_print(main, "loading config file : %s"%configFilePath)
        # attempt to open config file
        try:
            xmldoc = codecs.open(configFilePath,'r', 'utf-8')
            xmldoc = minidom.parseString(xmldoc.read().encode("utf-8"))
        except:
            utils.make_err_msg(
                _(u"Invalid XML in config file : %s") % configFilePath,
                _(u"Invalid Configuration")
            )
        else:
            config = xmldoc.firstChild

            # set autopreview to false while loading config
            # avoids loading paths more than once
            v = main.bottomWindow.autoPreview.GetValue()
            main.bottomWindow.autoPreview.SetValue(False)

            # get original path
            oldPath = main.picker.view.path.GetValue()

            self.__load_config_xml(config)

            # Do not replace a set path if one is not set in the config
            newPath = main.picker.view.path.GetValue()            
            if oldPath and not newPath:
                main.picker.view.path.SetValue(oldPath)

            # preview
            main.bottomWindow.autoPreview.SetValue(v)
            if main.autoModeLevel != 0 or\
             (main.prefs.get('previewOnConfig') and main.autoModeLevel is False):
                main.picker.view.reset_dirpicker_on_config_load()
