#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from PyQt4 import QtGui, QtCore
from PasswdController import PasswdController
from GroupsWidget import GroupsWidget

class PasswordsWidget(QtGui.QTableWidget):
    signalPasswdClicked = QtCore.pyqtSignal(int)
    
    def __init__(self, parent = None):
        self.__parent = parent
        self.__COL_TITLE = 0
        self.__COL_USERNAME = 1
        self.__COL_PASSWORD = 2
        self.__COL_URL = 3
        
        super(PasswordsWidget, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        """
            Initialize UI components.
        """
        # set column count
        self.setColumnCount(len(PasswdController.getTableColumns()))
        
        # set column names
        self.setHorizontalHeaderLabels(PasswdController.getTableColumns())
        
        # auto resize columns
        self.resizeColumnsToContents()
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        
        # not editable
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        
        # set connections
        self.cellClicked.connect(self.showDetails)
        self.cellDoubleClicked.connect(self.editPasswd)
        
        self.setMinimumWidth(400)
        
    def showPasswords(self, item_type, item_id):
        """
            Public slot to show passwords in table, whe signal emitPasswords(int, int)
            is emited.
            
            @param item_type: type of selected item (group, password, all)
            @param item_id: unique id from DB
        """
        # first remove all items
        self.removeAllRows()

        logging.debug("signal: type: %i, ID: %i", item_type, item_id)
        passwd_ctrl = PasswdController(self.__parent._db_ctrl, self.__parent._db_ctrl._master)
        
        # detect type
        if (item_type == GroupsWidget._TYPE_ALL):
            # select all
            passwords = passwd_ctrl.selectAll()
        elif (item_type == GroupsWidget._TYPE_GROUP):
            #select by group
            passwords = passwd_ctrl.selectByGroupId(item_id)
        elif (item_type == GroupsWidget._TYPE_PASS):
            #select just one password
            passwords = passwd_ctrl.selectById(item_id)
            
        self.__row_id_dic = {}
            
        # now fill passwords table view
        for passwd in passwords:
            row = self.rowCount()
            logging.debug("adding password: %s , at row: %i", passwd, row)
            self.insertRow(row)
       
            # set data
            self.setItem(row, self.__COL_TITLE, QtGui.QTableWidgetItem(passwd._title))
            self.setItem(row, self.__COL_USERNAME, QtGui.QTableWidgetItem(passwd._username))
            self.setItem(row, self.__COL_PASSWORD, QtGui.QTableWidgetItem(passwd._passwd))
            self.setItem(row, self.__COL_URL, QtGui.QTableWidgetItem(passwd._url))
            
            # save row id reference
            self.__row_id_dic[row] = passwd._id
    
    def removeAllRows(self):
        """
            Remove all items from table.
        """
        for i in range(0, self.rowCount()):
            self.removeRow(self.rowCount() - 1)
            
    def showDetails(self, row, column):
        logging.debug("clicked at item row: %i, column: %i, emiting ID: %i", row, column, self.__row_id_dic[row])
        
        self.signalPasswdClicked.emit(self.__row_id_dic[row])
        
    def editPasswd(self, row, column):
        logging.debug("double clicked at item row: %i, column: %i", row, column)