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
import logging
from PyQt4 import QtGui
from IconController import IconController
from TransController import tr
from SaveDialog import SaveDialog

class GroupDialog(SaveDialog):
    def __init__(self, db_ctrl):
        self.__db_ctrl = db_ctrl
        
        super(GroupDialog, self).__init__()
        
        self.initUi()
        self.center()
        self.initConnections()
        
    def initUi(self):
        """
            Initialize UI components.
        """
        SaveDialog.initUi(self)
        
        logging.info("initializing UI components.")
        
        # create lables
        name_label = QtGui.QLabel("<b>" + tr("Name:") + "</b>")
        description_label = QtGui.QLabel("<b>" + tr("Description:") + "</b>")
        icon_label = QtGui.QLabel("<b>" + tr("Icon:") + "</b>")
        
        self._layout_gl.addWidget(name_label, 0, 0)
        self._layout_gl.addWidget(description_label, 1, 0)
        self._layout_gl.addWidget(icon_label, 2, 0)
        
        # create inputs
        self._name = QtGui.QLineEdit()
        self._desc = QtGui.QLineEdit()
        self._icons = QtGui.QComboBox()
        
        self._layout_gl.addWidget(self._name, 0, 1)
        self._layout_gl.addWidget(self._desc, 1, 1)
        self._layout_gl.addWidget(self._icons, 2, 1)
        
    def initConnections(self):
        """
            Inialize event handlers.
        """
        SaveDialog.initConections(self)
        
        # when something changed, enable save button
        self._name.textChanged.connect(self.enableSaveButton)
        self._desc.textChanged.connect(self.enableSaveButton)
        self._icons.currentIndexChanged.connect(self.enableSaveButton)
        
    def loadIcons(self, i_id = False):
        """
            Load icons from DB to combobox. If is set i_id seti as current.
            
            @param i_id: current icon ID
        """
        # set groups combobox
        icon_ctrl = IconController(self.__db_ctrl)
        
        icons = icon_ctrl.selectAll()
        # tmp index
        tmp = 0
        # have to increment tmp
        inc_tmp = True
        
        # fill combobox
        for icon in icons:
            logging.info("adding icon ID: %d", icon._id)
            
            # load icon
            pix = QtGui.QPixmap()
            pix.loadFromData(icon._icon)
            
            # add item with icon, name and icon ID
            self._icons.addItem(QtGui.QIcon(pix), tr(icon._name), icon._id)
            
            if (i_id):
                # if a dont have curent index
                if (icon._id != i_id and inc_tmp):
                    tmp += 1
                    
                    logging.info("temp icon index: %d, icon._id: %d, i_id: %d", tmp, icon._id, i_id)
                else:
                    if inc_tmp:
                        logging.info("icon found")
                        inc_tmp = False
        # set current group
        if (i_id):
            self._icons.setCurrentIndex(tmp)
            
    def getIconId(self):
        """
            Get icon ID from combobox item.
            
            @return: icon ID
        """
        index = self._icons.currentIndex()
        
        # return a touple
        icon_id = self._icons.itemData(index).toInt()[0]
        
        logging.info("current item index: %d group: %d", index, icon_id)
        
        return icon_id