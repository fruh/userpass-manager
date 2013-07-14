#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    This file is part of UserPass Manager
    Copyright (C) 2013  Frantisek Uhrecky <frantisek.uhrecky[at]gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
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