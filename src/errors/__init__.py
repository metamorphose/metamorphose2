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

import classes
import wxErrorsView

class Parameters(classes.Parameters):
    """Handle loading parameters"""
    
    def __init__(self, Panel):
        # set the picker panel
        self.Panel = Panel
        # define the operation type used to retrieve values
        self.set_value_method()

    def load(self):
        """Load all needed panel values to instance."""
        widgets = (
            '',
        )
        return self.set_parameters(widgets)


# needs work, obviously
class Core():
    """Error core."""
    def __init__(self, parent, MainWindow):
        global main
        main = MainWindow
        self.Panel = wxErrorsView.Panel(self, parent, main)

    def show(self):
        """Show errors."""
        self.Panel.display_errors(main.errorLog, main.warn, main.bad)

    def clear(self):
        """Clear all errors"""
        self.Panel.clear_errors()
