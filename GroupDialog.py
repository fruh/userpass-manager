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