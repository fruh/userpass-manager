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
import logging
from TransController import tr

class SaveDialog(QtGui.QDialog):
    """
        Create an abtract dialog window, with grid layout to edit, and save and acancel buttons.
        On save returns accepted, on cancel rejected.
    """
    def __init__(self):
        super(SaveDialog, self).__init__()
        
    def initUi(self):
        """
            Initialize Ui components.
        """
        # not maximize, minimize buttons
        self.setWindowFlags(QtCore.Qt.Tool);
        
        main_layout = QtGui.QVBoxLayout()
        self.setLayout(main_layout)
    
        # create grid layout
        self._layout_gl = QtGui.QGridLayout()
        
        main_layout.addLayout(self._layout_gl)
        
        # create buttons
        self.__button_box = QtGui.QDialogButtonBox()
        
        self.__save_button = QtGui.QPushButton(tr("&Save"))
        self.__save_button.setEnabled(False)
        
        self.__cancel_button = QtGui.QPushButton(tr("&Cancel"))
        
        self.__button_box.addButton(self.__save_button, QtGui.QDialogButtonBox.AcceptRole)
        self.__button_box.addButton(self.__cancel_button, QtGui.QDialogButtonBox.RejectRole)
        
        main_layout.addWidget(self.__button_box, 0, QtCore.Qt.AlignRight)
        
    def initConections(self):
        """
            Initialize all connections, handling events.
            
            @requires: initUI(), setPassword() first
        """
        # connections to buttons
        self.__button_box.accepted.connect(self.saveChanges)
        self.__button_box.rejected.connect(self.reject)
        
    def enableSaveButton(self):
        """
            Enable save button.
        """
        if (not self.__save_button.isEnabled()):
            logging.info("enabling save button")
            
            self.__save_button.setEnabled(True)
            
    def disableSaveButton(self):
        """
            Disable save button.
        """
        if (self.__save_button.isEnabled()):
            logging.info("disabling save button")
            
            self.__save_button.setEnabled(False)
            
    def saveChanges(self):
        """
            @todo: Implement save matters. And accept dialog.
        """
        pass
    
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