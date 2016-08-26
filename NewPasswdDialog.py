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