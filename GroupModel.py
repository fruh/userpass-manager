#!/usr/bin/python
# -*- coding: utf-8 -*-
class GroupModel:
    """
        Holds Group data.
    """
    def __init__(self, g_id = None, name = None, description = None, icon_id = None):
        """
            Initialize GroupModel.
            
            @param g_id: group id
            @param name: group name
            @param description: group description
            @param icon_id: icon_id
        """
        self._id = g_id
        self._name = name
        self._description = description
        self._icon_id = icon_id
        
    def __str__(self):
        return "{'id' : '" + str(self._id) + "', 'name' : '" + self._name + "', 'description' : '" + self._description + "', 'icon_id' : '" + str(self._icon_id) + "'}" 