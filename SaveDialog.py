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