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
from TransController import tr
from GroupController import GroupController
import logging
import InfoMsgBoxes

class NewGroupDialog(GroupDialog):
    def __init__(self, parent):
        """
            Initialize group dailog for adding new groups
        """
        self.__parent = parent
        
        super(NewGroupDialog, self).__init__(parent._db_ctrl)
        self.loadIcons()
        self.disableSaveButton()
        
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
        try:
            group_ctrl = GroupController(self.__parent._db_ctrl)
            
            # prepare data
            name = str(self._name.text().toUtf8())
            desc = str(self._desc.text().toUtf8())
            icon_id = self.getIconId()
        
            group_ctrl.insertGroup(name, desc, icon_id)
            
            self.accept()
        except Exception as e:
            logging.exception(e)
            
            InfoMsgBoxes.showErrorMsg(e)