#!/usr/bin/python
#-*- coding: utf-8 -*-

import logging
from PyQt4 import QtGui, QtCore
from TransController import tr
from GroupController import GroupController
from IconController import IconController
from PasswdController import PasswdController

class GroupsWidget(QtGui.QTreeWidget):
    # private attr:
    __parent = None
    __COL_ICON = 0
    __COL_NAME = 1
    __COL_ID = 2
    __COL_TYPE = 3
    __TYPE_ALL = 1
    __TYPE_GROUP = 2
    __TYPE_PASS = 3
    
    def __init__(self, parent = None):
        self.__parent = parent
        super(GroupsWidget, self).__init__(parent)
        
        self.initUI()
        self.initItems()
        
        self.clicked.connect(self.showPasswords)
        
    def initUI(self):
        """
            Initialize groups tree widget, size etc.
        """
        logging.debug("Initialising UI components.")
        
        # remove header
        self.header().close()
        self.setColumnCount(2)
        # width for icon column
        self.setColumnWidth(0, 60)
        
    def initItems(self):
        """
            Initialize groups tree items. Load items from DB.
        """
        logging.debug("Adding items to tree.")
        group_ctrl = GroupController(self.__parent._db_ctrl)
        passwd_ctrl = PasswdController(self.__parent._db_ctrl, self.__parent._db_ctrl._master)
        icon_ctrl = IconController(self.__parent._db_ctrl)
        
        groups = group_ctrl.selectAll()
        
        # group, that contains all passwords
        all_group = self.initItemData(icon_ctrl.selectByName("key")._icon, 
                                      tr("All"), -1, tr("All passwords group."), self.__TYPE_ALL)
        self.addTopLevelItem(all_group)
        
        # add cildren, all passwords to group all
        passwords = passwd_ctrl.selectAll()
        
        for passwd in passwords:
            child = self.initItemData(passwd._grp._icon._icon, passwd._title, passwd._id, passwd._comment, self.__TYPE_PASS)
            
            all_group.addChild(child)
        
        # insert groups to tree
        for group in groups:
            item = self.initItemData(group._icon._icon, tr(group._name), group._id, group._description, self.__TYPE_GROUP)
            
            self.addTopLevelItem(item)
            
            # add cildren, all passwords to group all
            passwords = passwd_ctrl.selectByGroupId(group._id)
            
            for passwd in passwords:
                child = self.initItemData(passwd._grp._icon._icon, passwd._title, passwd._id, passwd._comment, self.__TYPE_PASS)
                
                item.addChild(child)
            
          
    def initItemData(self, icon, name, item_id, tooltip, item_type):
        """
            Initialize item data.
            
            @param icon: item icon data
            @param name: item name
            @param item_id: item group
            @param tooltip: tooltip string
            @param item_type: item type (pass, group, all)
            
            @return: QTreeWidgetItem object
        """
        item = QtGui.QTreeWidgetItem()
        
        # load image to display mode
        pix = QtGui.QPixmap()
        pix.loadFromData(icon)
        
        item.setIcon(self.__COL_ICON, QtGui.QIcon(pix))
        item.setText(self.__COL_NAME, tr(name))
        item.setData(self.__COL_NAME, QtCore.Qt.ToolTipRole, tooltip)
        item.setData(self.__COL_ID, QtCore.Qt.DisplayRole, item_id)
        item.setData(self.__COL_TYPE, QtCore.Qt.DisplayRole, item_type)
        
        return item
      
    def showPasswords(self, group):
        self.currentItemData(self.__COL_ID)
        self.currentItemData(self.__COL_NAME)
        self.currentItemData(self.__COL_TYPE)
        
              
    def currentItemData(self, col):
        """
            Get curent item type from __COL_TYPE
            
            @param col: column number
            
            @return: current item data col
        """
        # to int return a tuple
        if (col == self.__COL_ID):
            ret = self.currentItem().data(self.__COL_ID, QtCore.Qt.DisplayRole).toInt()[0]
        
            logging.debug("curent item ID: %i", ret)
        elif (col == self.__COL_NAME):
            ret = self.currentItem().data(self.__COL_NAME, QtCore.Qt.DisplayRole).toString()
        
            logging.debug("curent item name: %s", ret)
        elif (col == self.__COL_TYPE):
            ret = self.currentItem().data(self.__COL_TYPE, QtCore.Qt.DisplayRole).toInt()[0]
        
            logging.debug("curent item type: %i", ret)
        return ret