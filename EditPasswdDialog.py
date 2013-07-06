#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from PyQt4 import QtGui, QtCore
from PasswdController import PasswdController
import datetime
from GroupController import GroupController
from PasswdDialog import PasswdDialog

class EditPasswdDialog(PasswdDialog):
    def __init__(self, parent, p_id):
        self.__parent = parent
        super(EditPasswdDialog, self).__init__(parent._db_ctrl)
        
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
        self.setWindowTitle(self.__password._title)
        
        date_time_str = str(datetime.datetime.fromtimestamp(self.__password._e_date).strftime("%Y-%m-%d %H:%M:%S"))
        logging.debug("date time string: %s", date_time_str)
        
        self._title.setText(self.__password._title)
        self._username.setText(self.__password._username)
        self._passwd.setText(self.__password._passwd)
        self._url.setText(self.__password._url)
        self._c_date.setText(str(datetime.datetime.fromtimestamp(self.__password._c_date).strftime("%Y-%m-%d %H:%M:%S")))
        self._m_date.setText(str(datetime.datetime.fromtimestamp(self.__password._m_date).strftime("%Y-%m-%d %H:%M:%S")))
        self._e_date_edit.setDateTime(QtCore.QDateTime.fromString(date_time_str, "yyyy-MM-dd HH:mm:ss"))
        self._comment.setText(self.__password._comment)
        self._att_name.setText(self.__password._att_name)
        
        # set expiration button
        if (self.__password._expire == "false"):
            self._e_date_never.setChecked(True)
        else:
            self._e_date_never.setChecked(False)
        
        self.loadGroups()
        
        # disable save button, because nothing changed, just loaded from DB
        self.disableSaveButton()
        
    def loadGroups(self):
        """
            Load available groups to combobox
        """
        # set groups combobox
        group_ctrl = GroupController(self.__parent._db_ctrl)
        
        groups = group_ctrl.selectAll()
        # tmp index
        tmp = 0
        # have to increment tmp
        inc_tmp = True
        
        # fill combobox
        for group in groups:
            logging.debug("adding group ID: %d", group._id)
            
            # load icon
            pix = QtGui.QPixmap()
            pix.loadFromData(group._icon._icon)
            
            # add item with icon, name and group ID
            self._group.addItem(QtGui.QIcon(pix), group._name, group._id)
            
            # if a dont have curent group
            if (group._id != self.__password._grp._id and inc_tmp):
                tmp += 1
                
                logging.debug("temp group index: %d, group._id: %d, __password._grp._id: %d", tmp, group._id, self.__password._grp._id)
            else:
                if inc_tmp:
                    logging.debug("group found")
                    inc_tmp = False
        # set current group
        self._group.setCurrentIndex(tmp)
        
    def saveChanges(self):
        """
            Save changes to database, read all iinputs and update DB entry.
        """
        logging.debug("save button clicked.")
        
        self.__password._title = str(self._title.text())
        self.__password._username = str(self._username.text())
        self.__password._passwd = str(self._passwd.text())
        self.__password._url = str(self._url.text())
        self.__password._comment = str(self._comment.toPlainText())
        self.__password._att_name = str(self._att_name.text())
        
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
        
        # update password
        passwd_ctrl = PasswdController(self.__parent._db_ctrl, self.__parent._user._master)
        
        passwd_ctrl.updatePasswd(self.__password._id, self.__password._title, self.__password._username, self.__password._passwd, 
                                 self.__password._url, self.__password._comment, self.__password._e_date, 
                                 self.__password._grp._id, self.__password._user._id, self.__password._att_name, 
                                 self.__password._att_name, self.__password._expire)
        self.signalPasswdSaved.emit(self.__password._id)
        
        self.close()