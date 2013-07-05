#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from PyQt4 import QtGui, QtCore
from PasswdController import PasswdController
import datetime
from TransController import tr

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
        
        layout_gl.addWidget(title_label, 0, 0)
        layout_gl.addWidget(username_label, 1, 0)
        layout_gl.addWidget(passwd_label, 2, 0)
        layout_gl.addWidget(url_label, 3, 0)
        layout_gl.addWidget(c_date_label, 4, 0)
        layout_gl.addWidget(m_date_label, 5, 0)
        layout_gl.addWidget(e_date_label, 6, 0)
        layout_gl.addWidget(attachment_label, 7, 0)
        layout_gl.addWidget(comment_label, 8, 0)
        
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
        
        self.__attachment = QtGui.QLineEdit()
        
        layout_gl.addWidget(self.__title, 0, 1)
        layout_gl.addWidget(self.__username, 1, 1)
        layout_gl.addWidget(self.__passwd, 2, 1)
        layout_gl.addWidget(self.__url, 3, 1)
        layout_gl.addWidget(self.__c_date, 4, 1)
        layout_gl.addWidget(self.__m_date, 5, 1)
        layout_gl.addWidget(self.__attachment, 7, 1)
        layout_gl.addWidget(self.__comment, 8, 1)
        
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
        
        layout_gl.addWidget(self.__button_box, 9, 1)
        
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
        passwd = passwd_ctrl.selectById(p_id)[0]
        
        # set window title
        self.setWindowTitle(passwd._title)
        
        date_time_str = str(datetime.datetime.fromtimestamp(passwd._e_date).strftime("%Y-%m-%d %H:%M:%S"))
        logging.debug("date time string: %s", date_time_str)
        
        self.__title.setText(passwd._title)
        self.__username.setText(passwd._username)
        self.__passwd.setText(passwd._passwd)
        self.__url.setText(passwd._url)
        self.__c_date.setText(str(datetime.datetime.fromtimestamp(passwd._c_date).strftime("%Y-%m-%d %H:%M:%S")))
        self.__m_date.setText(str(datetime.datetime.fromtimestamp(passwd._m_date).strftime("%Y-%m-%d %H:%M:%S")))
        self.__e_date_edit.setDateTime(QtCore.QDateTime.fromString(date_time_str, "yyyy-MM-dd HH:mm:ss"))
        self.__comment.setText(passwd._comment)
        self.__attachment.setText(passwd._att_name)
        
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