#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from PyQt4 import QtGui, QtCore
from PasswdController import PasswdController
from GroupsWidget import GroupsWidget

class PasswordsWidget(QtGui.QTableWidget):
    # parameters are item ID
    signalPasswdClicked = QtCore.pyqtSignal(int)
    signalPasswdDoubleClicked = QtCore.pyqtSignal(int)
    
    def __init__(self, parent = None):
        self.__parent = parent
        self.__COL_TITLE = 0
        self.__COL_USERNAME = 1
        self.__COL_PASSWORD = 2
        self.__COL_URL = 3
        
        super(PasswordsWidget, self).__init__()
        
        self.initUI()
        self.initConections()
        
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
        
        self.setMinimumWidth(460)
        self.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        
    def initConections(self):
        """
            Initialize all connections, handling events.
            
            @requires: initUI() first
        """
        # set connections for editing password
        self.cellDoubleClicked.connect(self.editPasswd)
        
        # emits when slection cganged so (clicked, arrow move)
        self.itemSelectionChanged.connect(self.callShowDetails)
        
    def keyReleaseEvent(self, event):
        logging.debug("key pressed: %d", event.key())
        
        if (event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return):
            if (self.rowCount()):
                self.callEditPasswd()
            else:
                logging.debug("empty table")
        
    def showAll(self):
        """
            Show all passwords.
        """
        self.removeAllRows()
        
        passwd_ctrl = PasswdController(self.__parent._db_ctrl, self.__parent._db_ctrl._master)
        passwords = passwd_ctrl.selectAll()
        
        self.fillTable(passwords)
        
    def fillTable(self, passwords):
        """
            Insert passwords to table.
            
            @param passwords: passwords list
        """
        self.__row_id_dic = {}
            
        # now fill passwords table view
        for passwd in passwords:
            row = self.rowCount()
            logging.debug("adding password: %s , at row: %i", passwd, row)
            self.insertRow(row)
       
            pix = QtGui.QPixmap()
            pix.loadFromData(passwd._grp._icon._icon)
       
            # set data
            self.setItem(row, self.__COL_TITLE, QtGui.QTableWidgetItem((QtGui.QIcon(pix)), passwd._title))
            self.setItem(row, self.__COL_USERNAME, QtGui.QTableWidgetItem(passwd._username))
            self.setItem(row, self.__COL_PASSWORD, QtGui.QTableWidgetItem(passwd._passwd))
            self.setItem(row, self.__COL_URL, QtGui.QTableWidgetItem(passwd._url))
            
            # save row id reference
            self.__row_id_dic[row] = passwd._id
        
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
        self.fillTable(passwords)
    
    def removeAllRows(self):
        """
            Remove all items from table.
        """
        for i in range(0, self.rowCount()):
            self.removeRow(self.rowCount() - 1)
            
    def showDetails(self, row, column):
        logging.debug("item selection changed at item row: %i, column: %i, emiting ID: %i", row, column, self.__row_id_dic[row])
        
        self.signalPasswdClicked.emit(self.__row_id_dic[row])
        
    def editPasswd(self, row, column):
        logging.debug("double clicked or enter pressed at item row: %i, column: %i", row, column)
        
        self.signalPasswdDoubleClicked.emit(self.__row_id_dic[row])
        
    def callShowDetails(self):
        self.showDetails(self.currentRow(), self.currentColumn())
        
    def callEditPasswd(self):
        self.editPasswd(self.currentRow(), self.currentColumn())