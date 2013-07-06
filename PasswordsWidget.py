#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from PyQt4 import QtGui, QtCore
from PasswdController import PasswdController
from GroupsWidget import GroupsWidget

class PasswordsWidget(QtGui.QTableWidget):
    # parameters are item ID
    signalShowDetailPasswd = QtCore.pyqtSignal(int)
    # when double clicked
    signalEditPasswd = QtCore.pyqtSignal(int)
    
    def __init__(self, parent = None):
        self.__parent = parent
        self.__COL_TITLE = 0
        self.__COL_USERNAME = 1
        self.__COL_PASSWORD = 2
        self.__COL_URL = 3
        self.__COL_ID = 4
        
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
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(PasswdController.getTableColumns())
        
        # hide ID column
        self.hideColumn(self.__COL_ID)
        
        # auto resize columns
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.horizontalHeader().setMovable(True)
        
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
        """
            Handle release event to edit password, whe enter is pressed.
        """
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
        # disable sorting
        self.setSortingEnabled(False)
            
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
            self.setItem(row, self.__COL_ID, QtGui.QTableWidgetItem(str(passwd._id)))
        # enable sorting
        self.setSortingEnabled(True)
        
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
        # disable sorting
        self.setSortingEnabled(False)
        
        for i in range(0, self.rowCount()):
            self.removeRow(self.rowCount() - 1)
            
    def showDetails(self, row, column):
        p_id = self.item(row, self.__COL_ID).text().toInt()[0]
        logging.debug("item selection changed at item row: %i, column: %i, emiting ID: %i", row, column, p_id)
        
        self.signalShowDetailPasswd.emit(p_id)
        
    def editPasswd(self, row, column):
        logging.debug("double clicked or enter pressed at item row: %i, column: %i", row, column)
        
        self.signalEditPasswd.emit(self.item(row, self.__COL_ID).text().toInt()[0])
        
    def callShowDetails(self):
        self.showDetails(self.currentRow(), self.currentColumn())
        
    def callEditPasswd(self):
        self.editPasswd(self.currentRow(), self.currentColumn())