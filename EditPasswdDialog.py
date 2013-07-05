#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from PyQt4 import QtGui, QtCore
from PasswdController import PasswdController
import datetime
from TransController import tr
from GroupController import GroupController

class EditPasswdDialog(QtGui.QDialog):
    def __init__(self, db_ctrl, p_id):
        self.__db_ctrl = db_ctrl
        self.__p_id = p_id
        super(EditPasswdDialog, self).__init__()
        
        self.initUI()
        self.setPassword(p_id)
        self.initConections()
        
    def initUI(self):
        """
            Initilize UI components.
        """
        # not maximize, minimize buttons
        self.setWindowFlags( QtCore.Qt.Tool);
        
        self.center()
        
        layout_gl = QtGui.QGridLayout()
        self.setLayout(layout_gl)
        
        title_label = QtGui.QLabel("<b>" + tr("Title:") + "</b>")
        username_label = QtGui.QLabel("<b>" + tr("Username:") + "</b>")
        passwd_label = QtGui.QLabel("<b>" + tr("Password:") + "</b>")
        url_label = QtGui.QLabel("<b>" + tr("URL:")  + "</b>")
        c_date_label = QtGui.QLabel("<b>" + tr("Creation date:") + "</b>")
        m_date_label = QtGui.QLabel("<b>" + tr("Modification date:") + "</b>")
        e_date_label = QtGui.QLabel("<b>" + tr("Expiration date:") + "</b>")
        comment_label = QtGui.QLabel("<b>" + tr("Comment:") + "</b>")
        attachment_label = QtGui.QLabel("<b>" + tr("Attachment:") + "</b>")
        group_label = QtGui.QLabel("<b>" + tr("Groups:") + "</b>")
        
        layout_gl.addWidget(title_label, 0, 0)
        layout_gl.addWidget(username_label, 1, 0)
        layout_gl.addWidget(passwd_label, 2, 0)
        layout_gl.addWidget(url_label, 3, 0)
        layout_gl.addWidget(c_date_label, 4, 0)
        layout_gl.addWidget(m_date_label, 5, 0)
        layout_gl.addWidget(e_date_label, 6, 0)
        layout_gl.addWidget(attachment_label, 7, 0)
        layout_gl.addWidget(comment_label, 8, 0)
        layout_gl.addWidget(group_label, 9, 0)
        
        self.__title = QtGui.QLineEdit()
        self.__username = QtGui.QLineEdit()
        self.__passwd = QtGui.QLineEdit()
        self.__url = QtGui.QLineEdit()
        self.__c_date = QtGui.QLabel()
        self.__m_date = QtGui.QLabel()
        self.__e_date = QtGui.QLineEdit()
        self.__comment = QtGui.QTextEdit()
        self.__comment.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)
        self.__comment.setMaximumHeight(200)
        self.__group = QtGui.QComboBox()
        self.__attachment = QtGui.QLineEdit()
        
        layout_gl.addWidget(self.__title, 0, 1)
        layout_gl.addWidget(self.__username, 1, 1)
        layout_gl.addWidget(self.__passwd, 2, 1)
        layout_gl.addWidget(self.__url, 3, 1)
        layout_gl.addWidget(self.__c_date, 4, 1)
        layout_gl.addWidget(self.__m_date, 5, 1)
        layout_gl.addWidget(self.__attachment, 7, 1)
        layout_gl.addWidget(self.__comment, 8, 1)
        layout_gl.addWidget(self.__group, 9, 1)
        
        # date time edit
        self.__e_date_edit = QtGui.QDateTimeEdit()
        self.__e_date_edit.setCalendarPopup(True)
        
        # expiration date can't be lower than current date
        self.__e_date_edit.setMinimumDateTime(QtCore.QDateTime.currentDateTime())
        
        layout_gl.addWidget(self.__e_date_edit, 6, 1)
        
        # create buttons
        self.__button_box = QtGui.QDialogButtonBox()
        
        self.__save_button = QtGui.QPushButton(tr("&Save"))
        self.__save_button.setEnabled(False)
        
        self.__cancel_button = QtGui.QPushButton(tr("&Cancel"))
        
        self.__button_box.addButton(self.__save_button, QtGui.QDialogButtonBox.AcceptRole)
        self.__button_box.addButton(self.__cancel_button, QtGui.QDialogButtonBox.RejectRole)
        
        layout_gl.addWidget(self.__button_box, 10, 1)
        
    def initConections(self):
        """
            Initialize all connections, handling events.
            
            @requires: initUI(), setPassword() first
        """
        # connections to buttons
        self.__button_box.accepted.connect(self.saveChanges)
        self.__button_box.rejected.connect(self.close)
        
        # when something changed, enable save button
        self.__title.textChanged.connect(self.enableSaveButton)
        self.__username.textChanged.connect(self.enableSaveButton)
        self.__passwd.textChanged.connect(self.enableSaveButton)
        self.__url.textChanged.connect(self.enableSaveButton)
        self.__comment.textChanged.connect(self.enableSaveButton)
        self.__attachment.textChanged.connect(self.enableSaveButton)
        self.__e_date_edit.dateChanged.connect(self.enableSaveButton)
        self.__group.currentIndexChanged.connect(self.enableSaveButton)
        
    def enableSaveButton(self):
        """
            Enable save button.
        """
        if (not self.__save_button.isEnabled()):
            logging.debug("enabling save button")
            
            self.__save_button.setEnabled(True)
        
    def setPassword(self, p_id):
        """
            Show password detail with id p_id.
            
            @param p_id: password ID
        """
        logging.debug("password details ID: %i", p_id)
        
        passwd_ctrl = PasswdController(self.__db_ctrl, self.__db_ctrl._master)
        
        # select password
        self.__password = passwd_ctrl.selectById(p_id)[0]
        
        # set window title
        self.setWindowTitle(self.__password._title)
        
        date_time_str = str(datetime.datetime.fromtimestamp(self.__password._e_date).strftime("%Y-%m-%d %H:%M:%S"))
        logging.debug("date time string: %s", date_time_str)
        
        self.__title.setText(self.__password._title)
        self.__username.setText(self.__password._username)
        self.__passwd.setText(self.__password._passwd)
        self.__url.setText(self.__password._url)
        self.__c_date.setText(str(datetime.datetime.fromtimestamp(self.__password._c_date).strftime("%Y-%m-%d %H:%M:%S")))
        self.__m_date.setText(str(datetime.datetime.fromtimestamp(self.__password._m_date).strftime("%Y-%m-%d %H:%M:%S")))
        self.__e_date_edit.setDateTime(QtCore.QDateTime.fromString(date_time_str, "yyyy-MM-dd HH:mm:ss"))
        self.__comment.setText(self.__password._comment)
        self.__attachment.setText(self.__password._att_name)
        
        # set groups combobox
        group_ctrl = GroupController(self.__db_ctrl)
        
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
            self.__group.addItem(QtGui.QIcon(pix), group._name, group._id)
            
            # if a dont have curent group
            if (group._id != self.__password._grp._id and inc_tmp):
                tmp += 1
                
                logging.debug("temp group index: %d, group._id: %d, __password._grp._id: %d", tmp, group._id, self.__password._grp._id)
            else:
                if inc_tmp:
                    logging.debug("group found")
                    inc_tmp = False
        # set current group
        self.__group.setCurrentIndex(tmp)
        
    def getGroupId(self):
        """
            Get group ID from combobox item.
            
            @return: group ID
        """
        index = self.__group.currentIndex()
        
        # return a touple
        group_id = self.__group.itemData(index).toInt()[0]
        
        logging.debug("current item index: %d group: %d", index, group_id)
        
        return group_id
        
    def center(self):
        """
            Center window.
        """
        # get frame geometry
        wg = self.frameGeometry()
        
        # get screen center
        cs = QtGui.QDesktopWidget().availableGeometry().center()
        wg.moveCenter(cs)
        
        self.move(wg.topLeft())
        
    def saveChanges(self):
        """
            Save changes to database, read all iinputs and update DB entry.
        """
        logging.debug("save button clicked.")
        
        self.__password._title = str(self.__title.text())
        self.__password._username = str(self.__username.text())
        self.__password._passwd = str(self.__passwd.text())
        self.__password._url = str(self.__url.text())
        self.__password._comment = str(self.__comment.toPlainText())
        self.__password._att_name = str(self.__attachment.text())
         
        # get group
        group_ctrl = GroupController(self.__db_ctrl)
        self.__password._grp = group_ctrl.selectById(self.getGroupId())
         
        # set expiration date
        self.__password._e_date = self.__e_date_edit.dateTime().toTime_t()
        
        # update password
        passwd_ctrl = PasswdController(self.__db_ctrl, self.__db_ctrl._master)
        
        passwd_ctrl.updatePasswd(self.__password._id, self.__password._title, self.__password._username, self.__password._passwd, 
                                 self.__password._url, self.__password._comment, self.__password._e_date, 
                                 self.__password._grp._id, self.__password._user._id, self.__password._attachment, 
                                 self.__password._att_name)
        
        self.close()