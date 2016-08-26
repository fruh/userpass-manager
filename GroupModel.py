#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    MIT License

    Copyright (c) 2013-2016 Frantisek Uhrecky

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
from IconController import IconController
import sqlite3
import logging

class GroupModel:
    """
        Holds Group data.
    """
    def __init__(self, g_id = None, name = None, description = None, icon_id = None, db_ctrl = None):
        """
            Initialize GroupModel.
            
            @param g_id: group id
            @param name: group name
            @param description: group description
            @param icon_id: icon_id
            @param db_ctrl: DB controller
            
        """
        self._id = g_id
        self._name = name
        self._description = description
        self._icon = None
        
        # now load icon
        self.selectIcon(icon_id, db_ctrl)
        
    def selectIcon(self, icon_id, db_ctrl):
        """
            Load icon from database.
            
            @param icon_id: icon ID
            @param db_ctrl: DB controller
        """
        try:
            self._icon = IconController(db_ctrl).selectById(icon_id)
        except sqlite3.Error as e:
            logging.exception("icon with ID: %i, %s", icon_id, e)
            
            raise e
        
    def __str__(self):
        return "{'id' : '" + str(self._id) + "', 'name' : '" + self._name + "', 'description' : '" + self._description + "', 'icon_id' : '" + str(self._icon._id) + "'}" 