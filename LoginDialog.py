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
from PyQt4 import QtGui, QtCore
from TransController import tr
import logging
from LoginController import LoginController
import AppSettings
from CreateDbDialog import CreateDbDialog
import os
from MainWindow import MainWindow

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
        dir_path = AppSettings.APP_REL_ROOT + AppSettings.DEFAULT_DB
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
                QtGui.QMessageBox(QtGui.QMessageBox.Critical, tr("Wrong credentials!"), tr("Username or password are wrong.")).exec_()
        except Exception as e:
            MainWindow.showErrorMsg(e)
        
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