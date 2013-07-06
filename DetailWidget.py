#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from PyQt4 import QtGui, QtCore
from PasswdController import PasswdController
from TransController import tr
from GroupsWidget import GroupsWidget
import datetime

class DetailWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        self.__parent = parent
        super(DetailWidget, self).__init__(parent)
        
        self.initUI()
        
    def initUI(self):
        """
            Initilize UI components.
        """
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
        layout_gl.addWidget(c_date_label, 0, 2)
        layout_gl.addWidget(m_date_label, 1, 2)
        layout_gl.addWidget(e_date_label, 2, 2)
        layout_gl.addWidget(attachment_label, 3, 2)
        layout_gl.addWidget(comment_label, 4, 0)
        
        self.__title = QtGui.QLabel()
        self.__username = QtGui.QLabel()
        self.__passwd = QtGui.QLabel()
        self.__url = QtGui.QLabel()
        self.__c_date = QtGui.QLabel()
        self.__m_date = QtGui.QLabel()
        self.__e_date = QtGui.QLabel()
        self.__comment = QtGui.QTextEdit()
        self.__comment.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)
        self.__comment.setMaximumHeight(100)
        self.__comment.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        
        self.__attachment = QtGui.QLabel()
        
        layout_gl.addWidget(self.__title, 0, 1)
        layout_gl.addWidget(self.__username, 1, 1)
        layout_gl.addWidget(self.__passwd, 2, 1)
        layout_gl.addWidget(self.__url, 3, 1)
        layout_gl.addWidget(self.__c_date, 0, 3)
        layout_gl.addWidget(self.__m_date, 1, 3)
        layout_gl.addWidget(self.__e_date, 2, 3)
        layout_gl.addWidget(self.__attachment, 3, 3)
        layout_gl.addWidget(self.__comment, 4, 1, 1, 3)
        
        layout_gl.setColumnStretch(1, 1)
        layout_gl.setColumnStretch(3, 1)
        
        # hide, it is none passwd clicked
        self.setHidden(True)
        
    def setPassword(self, p_id):
        """
            Show password detail with id p_id.
            
            @param p_id: password ID
        """
        logging.debug("password details ID: %i", p_id)
        
        passwd_ctrl = PasswdController(self.__parent._db_ctrl, self.__parent._user._master)
        
        # select password
        passwd = passwd_ctrl.selectById(p_id)[0]
        
        self.__title.setText(passwd._title)
        self.__username.setText(passwd._username)
        self.__passwd.setText(passwd._passwd)
        self.__url.setText(passwd._url)
        self.__c_date.setText(str(datetime.datetime.fromtimestamp(passwd._c_date).strftime("%Y-%m-%d %H:%M:%S")))
        self.__m_date.setText(str(datetime.datetime.fromtimestamp(passwd._m_date).strftime("%Y-%m-%d %H:%M:%S")))
        
        if (passwd._expire == "false"):
            self.__e_date.setText(tr("Never"))
        else:
            self.__e_date.setText(str(datetime.datetime.fromtimestamp(passwd._e_date).strftime("%Y-%m-%d %H:%M:%S")))
        self.__comment.setText(passwd._comment)
        self.__attachment.setText(passwd._att_name)
        
        # now show details
        self.setHidden(False)
        
    def clearDetails(self):
        """
            CLear displayed details.
        """
        self.__title.setText("")
        self.__username.setText("")
        self.__passwd.setText("")
        self.__url.setText("")
        self.__c_date.setText("")
        self.__m_date.setText("")
        self.__e_date.setText("")
        self.__comment.setText("")
        self.__attachment.setText("")
        
    def handleType(self, item_type, item_id):
        """
            Handle signal from GroupsWidget, if it is clicked on password show detail, else do nothing.
            
            @param item_type: source type password, group, all
            @param item_id: item id, i.e. password ID
        """
        logging.debug("handling type: %i ID: %i", item_type, item_id)
        
        if (item_type == GroupsWidget._TYPE_PASS):
            # is password
            self.setPassword(item_id)
        else:
            # clear detials
            self.clearDetails()
            
            # hide details
            self.setHidden(True)