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

"""Operation definitions."""

import modification
import changeLength
import directory
import insert
import move
import replace
import swap
#import yourModuleName


defs = {_(u"directory") : (u"directory", _(u"Modify the directory structure (move items)")),
        _(u"replace") : (u"replace", _(u"Find text and replace it with text or sub-operation")),
        _(u"modifications") : (u"modification", _(u"Case changes, character conversions, etc...")),
        _(u"move text") : (u"move", _(u"Find text and move it")),
        _(u"swap") : (u"swap", _(u"Find two portions of text and swap them")),
        _(u"insert") : (u"insert", _(u"Insert text or sub-operation")),
        _(u"length") : (u"changeLength", _(u"Change the length of the item")),

        # plugins/extras
        #_(u"your module") : (u"yourModuleName", _(u"Your module's description")),
        }


def get_internal_name(name):
    """Get the operation name as within the application."""
    return defs[name][0]

def get_translated_name(opType):
    """Get the translated operation name from the operation type."""
    type = False
    for k, v in defs.iteritems():
        if v[0] == opType:
            type = k
    return type

def get_longest_name_length():
    """Get the length of the longest operation name."""
    length = 0
    for k in defs.keys():
        kLength = len(k)
        if kLength > length:
            length = kLength
    return length