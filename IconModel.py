#!/usr/bin/python
# -*- coding: utf-8 -*-
class IconModel:
    """
        Holds Icon data.
    """
    def __init__(self, i_id = None, icon = None):
        """
            Initialize IconModel.
            
            @param i_id: ivcon id
            @param icon: icon image
        """
        self._id = i_id
        self._icon = icon