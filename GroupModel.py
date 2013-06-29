#!/usr/bin/python
# -*- coding: utf-8 -*-
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