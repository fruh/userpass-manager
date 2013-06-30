#!/usr/bin/python
# -*- coding: utf-8 -*-
class IconModel:
    """
        Holds Icon data.
    """
    def __init__(self, i_id = None, name = None, icon = None):
        """
            Initialize IconModel.
            
            @param i_id: icon id
            @param name: icon name
            @param icon: icon image
        """
        self._id = i_id
        self._name = name
        self._icon = icon