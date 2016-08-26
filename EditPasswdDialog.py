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
from PyQt4 import QtCore
from PasswdController import PasswdController
import datetime
from GroupController import GroupController
from PasswdDialog import PasswdDialog
import InfoMsgBoxes

class EditPasswdDialog(PasswdDialog):
    def __init__(self, parent, p_id, show_pass = False):
        self.__parent = parent
        super(EditPasswdDialog, self).__init__(parent._db_ctrl, show_pass)
        
        self.setPassword(p_id)
        
    def setPassword(self, p_id):
        """
            Show password detail with id p_id.
            
            @param p_id: password ID
        """
        logging.debug("password details ID: %i", p_id)
        
        passwd_ctrl = PasswdController(self.__parent._db_ctrl, self.__parent._user._master)
        
        # select password
        self.__password = passwd_ctrl.selectById(p_id)[0]
        
        # set window title
        self.setWindowTitle(QtCore.QString.fromUtf8(self.__password._title))
        
        date_time_str = str(datetime.datetime.fromtimestamp(self.__password._e_date).strftime("%Y-%m-%d %H:%M:%S"))
        logging.debug("date time string: %s", date_time_str)
        
        self._title.setText(QtCore.QString.fromUtf8(self.__password._title))
        self._username.setText(QtCore.QString.fromUtf8(self.__password._username))
        self._passwd.setText(QtCore.QString.fromUtf8(self.__password._passwd))
        self._url.setText(QtCore.QString.fromUtf8(self.__password._url))
        self._c_date.setText(str(datetime.datetime.fromtimestamp(self.__password._c_date).strftime("%Y-%m-%d %H:%M:%S")))
        self._m_date.setText(str(datetime.datetime.fromtimestamp(self.__password._m_date).strftime("%Y-%m-%d %H:%M:%S")))
        self._e_date_edit.setDateTime(QtCore.QDateTime.fromString(date_time_str, "yyyy-MM-dd HH:mm:ss"))
        self._comment.setText(QtCore.QString.fromUtf8(self.__password._comment))
        self._att_name.setText(QtCore.QString.fromUtf8(self.__password._att_name))
        
        # set attachment data
        self._attachment_data = self.__password._attachment
        
        # set expiration button
        if (self.__password._expire == "false"):
            self._e_date_never.setChecked(True)
        else:
            self._e_date_never.setChecked(False)
        
        self.loadGroups(self.__password._grp._id)
        
        # disable save button, because nothing changed, just loaded from DB
        self.disableSaveButton()
        
    def saveChanges(self):
        """
            Save changes to database, read all iinputs and update DB entry.
        """
        logging.debug("save button clicked.")
        
        try:
            self.__password._title = str(self._title.text().toUtf8())
            self.__password._username = str(self._username.text().toUtf8())
            self.__password._passwd = str(self._passwd.text().toUtf8())
            self.__password._url = str(self._url.text().toUtf8())
            self.__password._comment = str(self._comment.toPlainText().toUtf8())
            self.__password._att_name = str(self._att_name.text().toUtf8())
            
            # set expiration
            if (self._e_date_never.isChecked()):
                self.__password._expire = "false"
            else:
                self.__password._expire = "true"
            
            # get group
            group_ctrl = GroupController(self.__parent._db_ctrl)
            self.__password._grp = group_ctrl.selectById(self.getGroupId())
             
            # set expiration date
            self.__password._e_date = self._e_date_edit.dateTime().toTime_t()
            
            # set attachment data
            self.__password._attachment = self._attachment_data
    
            # update password
            passwd_ctrl = PasswdController(self.__parent._db_ctrl, self.__parent._user._master)
            
            passwd_ctrl.updatePasswd(self.__password._id, self.__password._title, self.__password._username, self.__password._passwd, 
                                     self.__password._url, self.__password._comment, self.__password._e_date, 
                                     self.__password._grp._id, self.__password._user._id, self.__password._attachment, 
                                     self.__password._att_name, self.__password._expire)
            self.signalPasswdSaved.emit(self.__password._id)
            self.accept()
        except Exception as e:
            InfoMsgBoxes.showErrorMsg(e)