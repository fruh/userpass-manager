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
from PyQt4 import QtGui, QtCore
from TransController import tr
import logging
from LoginController import LoginController
import AppSettings
from CreateDbDialog import CreateDbDialog
import os
import InfoMsgBoxes
import time

class LoginDialog(QtGui.QDialog):
    """
        Login dialog window, serves login user, and create new user.
    """
    # emmitted signal, when successfuly logged user
    # first param is user name, and second master password
    signalSuccessfullyLogged = QtCore.pyqtSignal(str, str)
    
    def __init__(self, db_ctrl):
        self.__db_ctrl = db_ctrl
        
        super(LoginDialog, self).__init__()
        
        self.initUI()
        self.center()
        self.initConnections()
        
    def initUI(self):
        """
            Initialize UI components.
        """
        self.setWindowTitle(tr("Log in: ") + QtCore.QString.fromUtf8(os.path.basename(AppSettings.readDbFilePath())))
        self.setFixedSize(500, 100)
        
        # create main grid layout
        layout_gl = QtGui.QGridLayout()
        self.setLayout(layout_gl)
        
        # labels
#         username_label = QtGui.QLabel("<b>" + tr("Username:") + "</b>")
        passwd_label = QtGui.QLabel("<b>" + tr("Password:") + "</b>")
        
        # add to layout
#         layout_gl.addWidget(username_label, 0, 0)
        layout_gl.addWidget(passwd_label, 0, 0)
        
#         self._username = QtGui.QLineEdit()
#         layout_gl.addWidget(self._username, 0, 1)
        
        self._passwd = QtGui.QLineEdit()
        
        # hide password
        self._passwd.setEchoMode(QtGui.QLineEdit.Password)
        
        # password layout
        passwd_hl = QtGui.QHBoxLayout()
        
        # add password edit line to layout
        passwd_hl.addWidget(self._passwd)
        
        # password visibility check box
        self._show_passwd_check = QtGui.QCheckBox(tr("Show"))
        self._show_passwd_check.setChecked(False)
        passwd_hl.addWidget(self._show_passwd_check)
        
        layout_gl.addLayout(passwd_hl, 0, 1)
        
        # create buttons
        self._button_box = QtGui.QDialogButtonBox()
        
        self.__login_button = QtGui.QPushButton(tr("&Log In"))
        self.__login_button.setEnabled(False)
        
        self.__close_button = QtGui.QPushButton(tr("&Close"))
        
        self._button_box.addButton(self.__login_button, QtGui.QDialogButtonBox.AcceptRole)
        self._button_box.addButton(self.__close_button, QtGui.QDialogButtonBox.RejectRole)
        
#         layout_gl.addWidget(self._button_box, 1, 1)
        
        # db button layout
        db_buttons_hl = QtGui.QHBoxLayout()
    
        self.__open_db = QtGui.QPushButton(tr("Open Database"))
        self.__create_db = QtGui.QPushButton(tr("Create Database"))
        
        db_buttons_hl.addWidget(self.__open_db)
        db_buttons_hl.addWidget(self.__create_db)
        db_buttons_hl.addWidget(self._button_box)
        
        layout_gl.addLayout(db_buttons_hl, 1, 0, 1, 2)
        
    def initConnections(self):
        """
            Init connections, reaction on signals.
        """
        # show/hide password
        self._show_passwd_check.stateChanged.connect(self.setVisibilityPass)
        
        # enable loggin button
#         self._username.textChanged.connect(self.enableCreateButton)
        self._passwd.textChanged.connect(self.enableCreateButton)
        
        # button connections
        self._button_box.rejected.connect(QtGui.QApplication.exit)
        self._button_box.accepted.connect(self.logIn)
        
        # db buttons connections
        self.__open_db.clicked.connect(self.selectDB)
        self.__create_db.clicked.connect(self.createDB)
        
    def enLogIn(self, b = True):
        """
            Enable or disable password input, show checkbox and login button.
        """
        logging.debug("enabling login: %s", b)
        
        self._passwd.setEnabled(b)
        self._show_passwd_check.setEnabled(b)
        self.__login_button.setEnabled(b)
        
        if (not b):
            self.setWindowTitle(tr("Database not selected."))
        else:
            self.setWindowTitle(tr("Log in: ") + QtCore.QString.fromUtf8(os.path.basename(AppSettings.readDbFilePath())))
        
    def selectDB(self):
        """
            Select database file.
        """
        dir_path = AppSettings.APP_ABS_ROOT + AppSettings.DEFAULT_DB
        file_path = QtGui.QFileDialog.getOpenFileName(self, tr("Select database"), QtCore.QString.fromUtf8(dir_path))
        
        if (not file_path.isEmpty()):
            db_path = str(file_path.toUtf8())
            
            logging.debug("database file path: %s", db_path)
            
            # write to setting file
            AppSettings.writeDbFilePath(db_path)
            
            self.enLogIn()
        else:
            logging.debug("database not selected")
        
    def createDB(self):
        """
            Create database.
        """
        logging.debug("create DB clicked")
        create_dialog = CreateDbDialog(self.__db_ctrl)
        
        # when created enable buttons
        create_dialog.signalDbCreated.connect(self.enLogIn)
        
        create_dialog.exec_()
        
    def logIn(self):
        """
            Read input lines and login user if possible.
        """
        logging.debug("logging user ...")
        
        try:
            path = AppSettings.readDbFilePath()
            self.__db_ctrl.connectDB(path)
            
            login_ctrl = LoginController(self.__db_ctrl)
            
            username = AppSettings.USER_NAME
            master = str(self._passwd.text().toUtf8())
            
            logged_user = login_ctrl.logInUser(username, master)
            
            if (logged_user):
                self.signalSuccessfullyLogged.emit(QtCore.QString.fromUtf8(username), QtCore.QString.fromUtf8(master))
                
                self.close()
            else:
                # sleep for a while
                time.sleep(AppSettings.WRONG_PASWD_SLEEP)
                
                # show message
                QtGui.QMessageBox(QtGui.QMessageBox.Critical, tr("Wrong credentials!"), tr("Username or password are wrong.")).exec_()
        except Exception as e:
            InfoMsgBoxes.showErrorMsg(e)
        
    def setVisibilityPass(self, state):
        """
            Set visibility password, depends on checkbox.
        """
        if (state == QtCore.Qt.Checked):
            self._passwd.setEchoMode(QtGui.QLineEdit.Normal)
        else:
            self._passwd.setEchoMode(QtGui.QLineEdit.Password)
        
    def enableCreateButton(self):
        """
            Enable login button. If is empty one of username or password, then disable.
        """
        if (self._passwd.text().isEmpty()):
            if (self.__login_button.isEnabled()):
                logging.debug("disabling login button")
                
                self.__login_button.setEnabled(False)
        else:
            if (not self.__login_button.isEnabled()):
                logging.debug("enabling login button")
                
                self.__login_button.setEnabled(True)
        
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