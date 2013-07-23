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
from PasswdController import PasswdController
import time
from PasswdDialog import PasswdDialog
import InfoMsgBoxes

class NewPasswdDialog(PasswdDialog):
    def __init__(self, parent, g_id = False, show_pass = False):
        self.__parent = parent
        super(NewPasswdDialog, self).__init__(parent._db_ctrl, show_pass, False)

        self.loadGroups(g_id)

    def saveChanges(self):
        """
            Save changes to database, read all iinputs and insert DB entry.
        """
        logging.debug("save button clicked.")
        
        try:
            title = str(self._title.text().toUtf8())
            username = str(self._username.text().toUtf8())
            passwd = str(self._passwd.text().toUtf8())
            url = str(self._url.text().toUtf8())
            comment = str(self._comment.toPlainText().toUtf8())
            att_name = str(self._att_name.text().toUtf8())
            attachment = self._attachment_data
             
            # get group
            grp_id = self.getGroupId()
             
            # creation date now
            c_date = time.time()
             
            # set expiration date
            e_date = self._e_date_edit.dateTime().toTime_t()
            
            # set expiration
            if (self._e_date_never.isChecked()):
                expire = "false"
            else:
                expire = "true"
            
            # update password
            passwd_ctrl = PasswdController(self.__parent._db_ctrl, self.__parent._user._master)
            
            passwd_ctrl.insertPassword(title, username, passwd, 
                                     url, comment, c_date, e_date, 
                                     grp_id, self.__parent._user._id, attachment, 
                                     att_name, expire)
            self.accept()
        except Exception as e:
            logging.exception(e)
            
            InfoMsgBoxes.showErrorMsg(e)