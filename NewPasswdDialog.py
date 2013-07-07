#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from PasswdController import PasswdController
import time
from PasswdDialog import PasswdDialog

class NewPasswdDialog(PasswdDialog):
    def __init__(self, parent, g_id = False):
        self.__parent = parent
        super(NewPasswdDialog, self).__init__(parent._db_ctrl, False)

        self.loadGroups(g_id)

    def saveChanges(self):
        """
            Save changes to database, read all iinputs and insert DB entry.
        """
        logging.debug("save button clicked.")
        
        title = str(self._title.text())
        username = str(self._username.text())
        passwd = str(self._passwd.text())
        url = str(self._url.text())
        comment = str(self._comment.toPlainText())
        att_name = str(self._att_name.text())
        attachment = ""
         
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
        self.signalPasswdSaved.emit(-1)
        
        self.close()