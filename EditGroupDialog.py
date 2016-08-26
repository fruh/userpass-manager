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
from GroupDialog import GroupDialog
from PyQt4 import QtCore
from TransController import tr
from GroupController import GroupController
import logging
import InfoMsgBoxes

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
        
        self.setWindowTitle(QtCore.QString.fromUtf8(tr("Edit group")) + ": " + QtCore.QString.fromUtf8(tr(self.__group._name)))
        
    def saveChanges(self):
        """
            Method for saving changes into db.
        """
        try:
            group_ctrl = GroupController(self.__parent._db_ctrl)
            
            # prepare data
            self.__group._name = str(self._name.text().toUtf8())
            self.__group._description = str(self._desc.text().toUtf8())
            icon_id = self.getIconId()
        
            group_ctrl.updateGroup(self.__group._id, self.__group._name, self.__group._description, icon_id)
            
            self.accept()
            
        except Exception as e:
            logging.exception(e)
            
            InfoMsgBoxes.showErrorMsg(e)