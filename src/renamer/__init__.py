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

import engine
import operations
import preview
import wxRenamerView


class Core():
    """
    Renamer controller.

    Allows interaction with renaming panel (view).
    Handles high level previewing and renaming of items.
    """
    def __init__(self, parent, MainWindow):
        global main
        main = MainWindow
        self.operations = [] # operations stack
        self.view = wxRenamerView.Panel(self, parent, main)
        self.__preview = preview.Core(main)
        self.__engine = engine.Core(main)

    def create_operation(self, n, opName, params={}):
        """Create a new instance of the specified operation and returns it."""
        opName = operations.get_internal_name(opName)
        # init operation object
        operation = getattr(operations, opName)
        # init operation panel object
        opPanel = operation.OpPanel(self.view, main, params)

        self.insert_operation(n, opPanel)
        return opPanel


    ## == View related methods == ##

    def destroy_all_operations(self):
        for n in range(len(self.operations)):
            self.operations[n].Destroy()
        self.operations = []

    def move_operations(self, n, moveTo):
        oldPanel = self.operations[n]
        del self.operations[n]
        self.operations.insert(moveTo, oldPanel)

    def delete_operation(self, n):
        self.operations[n].Destroy()
        del self.operations[n]

    def insert_operation(self, n, opPanel):
        self.operations.insert(n, opPanel)


    ## == Renaming related methods == ##

    def preview(self, event):
        self.__preview.setup()
        self.__preview.generate_names(event)

    def error_check_items(self):
        self.__preview.setup()
        self.__preview.error_check_items()

    def rename(self, event):
        self.__engine.rename(event)

    def undo(self, event):
        self.__engine.undo_last_rename(event)
