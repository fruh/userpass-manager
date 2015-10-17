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
    
def showErrorMsg(msg):
    """
        Display error message box.
    """
    QtGui.QMessageBox(QtGui.QMessageBox.Critical, tr("Something is wrong!"), tr("Something is wrong in program. Sorry.") + 
            "\n\n" + QtCore.QString.fromUtf8(str(msg))).exec_()
            
def showInfoMsg(msg):
    """
        Display error message box.
    """
    QtGui.QMessageBox(QtGui.QMessageBox.Information, tr("Information"), QtCore.QString.fromUtf8(str(msg))).exec_()