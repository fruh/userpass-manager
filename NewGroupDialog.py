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
import logging
from PyQt4 import QtGui, QtCore
from GroupDialog import GroupDialog
from TransController import tr
from GroupController import GroupController

class NewGroupDialog(GroupDialog):
    def __init__(self, parent, i_id = False):
        """
            Initialize group dailog for adding new groups
        """
        self.__parent = parent
        
        super(NewGroupDialog, self).__init__(parent._db_ctrl)
        self.loadIcons(i_id)
        
    def initUi(self):
        """
            Initialize UI components
        """
        # first call parent initialization.
        GroupDialog.initUi(self)
        
        self.setWindowTitle(tr("Add new group"))
        
    def saveChanges(self):
        """
            Method for saving changes into db.
        """
        group_ctrl = GroupController(self.__parent._db_ctrl)
        
        # prepare data
        name = str(self._name.text().toUtf8())
        desc = str(self._desc.text().toUtf8())
        icon_id = self.getIconId()
        
        try:
            group_ctrl.insertGroup( name, desc, icon_id)
            
            self.signalSaveClicked.emit()
            self.close()
            
        except Exception as e:
            logging.exception(e)
            
            raise e