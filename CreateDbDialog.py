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
from UserController import UserController
import AppSettings
import os

class CreateDbDialog(QtGui.QDialog):
    """
        Create DB dialog window, creates new database, so new file and new master password.
    """
    signalDbCreated = QtCore.pyqtSignal()
    
    def __init__(self, db_ctrl):
        """
            @param db_ctrl: database controller
        """
        self.__db_ctrl = db_ctrl
        
        super(CreateDbDialog, self).__init__()
        
        self.initUI()
        self.center()
        self.initConnections()
        
    def initUI(self):
        """
            Initialize UI components.
        """
        self.setWindowTitle(tr("Create Database"))
        self.setFixedSize(500, 150)
        
        # create main grid layout
        layout_gl = QtGui.QGridLayout()
        self.setLayout(layout_gl)
        
        # labels
        db_path_label = QtGui.QLabel("<b>" + tr("DB file path:") + "</b>")
        layout_gl.addWidget(db_path_label, 0, 0)
        
        passwd_label = QtGui.QLabel("<b>" + tr("New master password:") + "</b>")
        layout_gl.addWidget(passwd_label, 1, 0)
    
        # db line edit
        self._db_file_path = QtGui.QLineEdit()
    
        db_layout_hl = QtGui.QHBoxLayout()
        db_layout_hl.addWidget(self._db_file_path)
        
        # select file button
        self._select_db_button = QtGui.QPushButton(tr("Select file"))
        db_layout_hl.addWidget(self._select_db_button)
    
        layout_gl.addLayout(db_layout_hl, 0, 1)
        
        # password edit line
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
        
        layout_gl.addLayout(passwd_hl, 1, 1)
        
        # create buttons
        self._button_box = QtGui.QDialogButtonBox()
        
        self.__create_button = QtGui.QPushButton(tr("&Create"))
        self.__create_button.setEnabled(False)
        
        self.__close_button = QtGui.QPushButton(tr("&Close"))
        
        self._button_box.addButton(self.__create_button, QtGui.QDialogButtonBox.AcceptRole)
        self._button_box.addButton(self.__close_button, QtGui.QDialogButtonBox.RejectRole)
        
        layout_gl.addWidget(self._button_box, 2, 1)
        
        # db button box
        self._db_button_box = QtGui.QDialogButtonBox()
    
        self.__open_db = QtGui.QPushButton(tr("Open Database"))
        self.__create_db = QtGui.QPushButton(tr("Create Database"))
        
    def initConnections(self):
        """
            Init connections, reaction on signals.
        """
        # show/hide password
        self._show_passwd_check.stateChanged.connect(self.setVisibilityPass)
        
        # enable loggin button
        self._db_file_path.textChanged.connect(self.enableCreateButton)
        self._passwd.textChanged.connect(self.enableCreateButton)
        
        # button connections
        self._button_box.rejected.connect(self.close)
        self._button_box.accepted.connect(self.createDB)

        self._select_db_button.clicked.connect(self.selectFile)
        
    def selectFile(self):
        """
            Select DB file.
        """
        dir_path = AppSettings.APP_ABS_ROOT + AppSettings.DEFAULT_DB
        
        file_path = QtGui.QFileDialog.getSaveFileName(self, tr("Save DB file"), QtCore.QString.fromUtf8(dir_path))
        
        logging.debug("save db to file: %s", file_path)
        
        if (not file_path.isEmpty()):
            file_path = str(file_path.toUtf8())
            logging.debug("db file path: %s", file_path)
            
            self._db_file_path.setText(QtCore.QString.fromUtf8(file_path))
            
            if (os.path.exists(file_path)):
                logging.debug("removing existing file: '%s'", file_path)
                os.remove(file_path)
        else:
            logging.debug("db file not selected")
        
    def createDB(self):
        """
            Create DB file and new user with master password.
        """
        db_path = str(self._db_file_path.text().toUtf8())
        
        logging.debug("creating new DB: '%s'", db_path)
        
        # write to setting file
        AppSettings.writeDbFilePath(db_path)
        
        self.__db_ctrl.connectDB(db_path)
        self.__db_ctrl.createTables()
        self.__db_ctrl.insertDefRows()
        
        logging.debug("inserting user to DB: '%s'", AppSettings.USER_NAME)
        
        master = str(self._passwd.text().toUtf8())
        
        user = UserController(self.__db_ctrl)
        user.insertUser(AppSettings.USER_NAME, master)
        
        self.signalDbCreated.emit()
        self.close()
        
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
        if (self._passwd.text().isEmpty() or self._db_file_path.text().isEmpty()):
            if (self.__create_button.isEnabled()):
                logging.debug("disabling create button")
                
                self.__create_button.setEnabled(False)
        else:
            if (not self.__create_button.isEnabled()):
                logging.debug("enabling create button")
                
                self.__create_button.setEnabled(True)
        
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