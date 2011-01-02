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

import wx
import os

class Operation(wx.Panel):
    """"
    Base class for all operations.

    TODO - a lot !
    """
    def __init__(self, params={}):
        # default parameters
        # need to define here due to python's handling of class instances
        self.params = {
            'applyPathOnly' : False,
            'applyName' : True,
            'applyExtension' : False,
        }
        self.update_parameters(params)

    def update_parameters(self, params):
        """
        Allow passed-in parameters to overide defaults or add additional
        parameters
        """
        for k in params.keys():
            self.params[k] = params[k]

    def set_as_path_only(self):
        """Operations that only modify the path (e.g. 'directory')."""
        self.params['applyPathOnly'] = True
        self.params['applyName'] = False
        self.params['applyExtension'] = False

    def join_ext(self, name, ext):
        """Join extensions."""
        if self.params['applyName'] and not self.params['applyExtension']:
            newName = name
        elif self.params['applyExtension'] and not self.params['applyName']:
            newName = ext
        elif self.params['applyName'] and self.params['applyExtension']:
            if ext != '':
                newName = name+'.'+ext
            else:
                newName = name
        else:
            newName = False
        return newName

    def split_ext(self, newName, name, ext):
        """Split extensions."""
        if self.params['applyName'] and not self.params['applyExtension']:
            name = newName
        elif self.params['applyExtension'] and not self.params['applyName']:
            ext = newName
        elif self.params['applyName'] and self.params['applyExtension']:
            name = os.path.splitext(newName)[0]
            ext = os.path.splitext(newName)[1][1:]
        return name,ext
