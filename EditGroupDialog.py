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
from GroupDialog import GroupDialog
from PyQt4 import QtCore
from TransController import tr
from GroupController import GroupController
import logging

class EditGroupDialog(GroupDialog):
    def __init__(self, parent, g_id):
        """
            Initialize group dailog for editting groups
            
            @param parent: object containing _db_ctrl attribute, DB controller
            @param g_id: group ID to edit
        """
        self.__parent = parent
        self.__group = None
        self.loadGroup(g_id)
        
        super(EditGroupDialog, self).__init__(parent._db_ctrl)
        
        self.setGroup()
        self.disableSaveButton()
    
    def loadGroup(self, g_id):
        """
            Load group with ID.
            
            @param g_id: group ID
        """
        logging.info("loading group with ID: '%i'", g_id)
        group_ctrl = GroupController(self.__parent._db_ctrl)
        
        self.__group = group_ctrl.selectById(g_id)
        
    def setGroup(self):
        """
            Set loaded group to inputs.
        """
        # set names
        self._name.setText(QtCore.QString.fromUtf8(tr(self.__group._name)))
        self._desc.setText(QtCore.QString.fromUtf8(tr(self.__group._description)))
        
        # load icons and set current icon
        self.loadIcons(self.__group._icon._id)
    
    def initUi(self):
        """
            Initialize UI.
        """
        GroupDialog.initUi(self)
        
        self.setWindowTitle(tr("Edit group: ") + QtCore.QString.fromUtf8(tr(self.__group._name)))
        
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
            group_ctrl.updateGroup(self.__group._id, name, desc, icon_id)
            
            self.signalSaveClicked.emit()
            self.close()
            
        except Exception as e:
            logging.exception(e)
            
            raise e