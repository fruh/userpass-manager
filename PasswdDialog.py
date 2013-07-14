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
from PyQt4 import QtGui, QtCore
from TransController import tr
from GroupController import GroupController
import os

class PasswdDialog(QtGui.QDialog):
    # emiting after saving passowrd
    # param: p_id
    signalPasswdSaved = QtCore.pyqtSignal(int)
    
    def __init__(self, db_ctrl, show_pass = False, edit = True):
        """
            COnstructor for password dialog, displys all necessary inputs.
            
            @param db_ctrl: database controller
            @param edit: if it will we edit dialog, show creation and modification date, else do not
            @param show_pass: show password in visible form
        """
        self.__db_ctrl = db_ctrl
        self.__edit = edit
        self.__show_pass = show_pass
        super(PasswdDialog, self).__init__()
        
        self.initUI()
        self.initConections()
        self.center()
        
        # dafult never expire password
        self._e_date_never.setChecked(True)
        
        # intialize variables
        self._attachment_data = ""
        
    def initUI(self):
        """
            Initilize UI components.
        """
        # not maximize, minimize buttons
        self.setWindowFlags(QtCore.Qt.Tool);
        
        layout_gl = QtGui.QGridLayout()
        self.setLayout(layout_gl)
        
        title_label = QtGui.QLabel("<b>" + tr("Title:") + "</b>")
        username_label = QtGui.QLabel("<b>" + tr("Username:") + "</b>")
        passwd_label = QtGui.QLabel("<b>" + tr("Password:") + "</b>")
        url_label = QtGui.QLabel("<b>" + tr("URL:")  + "</b>")
        
        if (self.__edit):
            # if it is edit dialog display
            layout_offset = 0
            
            c_date_label = QtGui.QLabel("<b>" + tr("Creation date:") + "</b>")
            m_date_label = QtGui.QLabel("<b>" + tr("Modification date:") + "</b>")
            
            layout_gl.addWidget(c_date_label, 4, 0)
            layout_gl.addWidget(m_date_label, 5, 0)
            
            self._c_date = QtGui.QLabel()
            self._m_date = QtGui.QLabel()
            
            layout_gl.addWidget(self._c_date, 4, 1)
            layout_gl.addWidget(self._m_date, 5, 1)
        else:
            layout_offset = -2
            
        e_date_label = QtGui.QLabel("<b>" + tr("Expiration date:") + "</b>")
        comment_label = QtGui.QLabel("<b>" + tr("Comment:") + "</b>")
        attachment_label = QtGui.QLabel("<b>" + tr("Attachment:") + "</b>")
        group_label = QtGui.QLabel("<b>" + tr("Groups:") + "</b>")
        
        layout_gl.addWidget(title_label, 0, 0)
        layout_gl.addWidget(username_label, 1, 0)
        layout_gl.addWidget(passwd_label, 2, 0)
        layout_gl.addWidget(url_label, 3, 0)
        layout_gl.addWidget(e_date_label, 6 + layout_offset, 0)
        layout_gl.addWidget(attachment_label, 7 + layout_offset, 0)
        layout_gl.addWidget(comment_label, 9 + layout_offset, 0)
        layout_gl.addWidget(group_label, 10 + layout_offset, 0)
        
        self._title = QtGui.QLineEdit()
        self._username = QtGui.QLineEdit()
        self._passwd = QtGui.QLineEdit()
        
        if (not self.__show_pass):
            self._passwd.setEchoMode(QtGui.QLineEdit.Password)
        
        # password layout
        passwd_hl = QtGui.QHBoxLayout()
        passwd_hl.addWidget(self._passwd)
        
        # password visibility check box
        self._show_passwd_check = QtGui.QCheckBox(tr("Show"))
        self._show_passwd_check.setChecked(self.__show_pass)
        passwd_hl.addWidget(self._show_passwd_check)
              
        self._url = QtGui.QLineEdit()
        self._e_date = QtGui.QLineEdit()
        self._comment = QtGui.QTextEdit()
        self._comment.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)
        self._comment.setMaximumHeight(200)
        self._group = QtGui.QComboBox()
        self._att_name = QtGui.QLineEdit()
        self._att_name.setEnabled(False)
        
        layout_gl.addWidget(self._title, 0, 1)
        layout_gl.addWidget(self._username, 1, 1)
        layout_gl.addLayout(passwd_hl, 2, 1)
        layout_gl.addWidget(self._url, 3, 1)
        
        # attachment layout
        att_hl = QtGui.QHBoxLayout()
        
        # open file button
        self._att_button = QtGui.QPushButton(tr("New"))
        self._att_del_button = QtGui.QPushButton(tr("Del"))
        self._att_save_button = QtGui.QPushButton(tr("Save"))
        
        self._att_del_button.setEnabled(False)
        self._att_save_button.setEnabled(False)
        
        att_hl.addWidget(self._att_button)
        att_hl.addWidget(self._att_del_button)
        att_hl.addWidget(self._att_save_button)
        
        layout_gl.addWidget(self._att_name, 7 + layout_offset, 1)
        layout_gl.addLayout(att_hl, 8 + layout_offset, 1)
        layout_gl.addWidget(self._comment, 9 + layout_offset, 1)
        layout_gl.addWidget(self._group, 10 + layout_offset, 1)
        
        # date time edit
        self._e_date_edit = QtGui.QDateTimeEdit()
        self._e_date_edit.setCalendarPopup(True)
        
        # expiration date can't be lower than current date
        self._e_date_edit.setMinimumDateTime(QtCore.QDateTime.currentDateTime())
        
        # create never check box
        self._e_date_never = QtGui.QCheckBox(tr("Never"))
        
        # create horizontal layout for date selector and never check box
        e_date_hl = QtGui.QHBoxLayout()
        e_date_hl.addWidget(self._e_date_edit)
        e_date_hl.addWidget(self._e_date_never)
        
        # add to main layout
        layout_gl.addLayout(e_date_hl, 6 + layout_offset, 1)
        
        # create buttons
        self.__button_box = QtGui.QDialogButtonBox()
        
        self.__save_button = QtGui.QPushButton(tr("&Save"))
        self.__save_button.setEnabled(False)
        
        self.__cancel_button = QtGui.QPushButton(tr("&Cancel"))
        
        self.__button_box.addButton(self.__save_button, QtGui.QDialogButtonBox.AcceptRole)
        self.__button_box.addButton(self.__cancel_button, QtGui.QDialogButtonBox.RejectRole)
        
        layout_gl.addWidget(self.__button_box, 11 + layout_offset, 1)
        
    def setVisibilityPass(self, state):
        """
            Set no visible password and username.
        """
        if (state == QtCore.Qt.Checked):
            self._passwd.setEchoMode(QtGui.QLineEdit.Normal)
        else:
            self._passwd.setEchoMode(QtGui.QLineEdit.Password)
        
    def initConections(self):
        """
            Initialize all connections, handling events.
            
            @requires: initUI(), setPassword() first
        """
        # connections to buttons
        self.__button_box.accepted.connect(self.saveChanges)
        self.__button_box.rejected.connect(self.close)
        
        # when something changed, enable save button
        self._title.textChanged.connect(self.enableSaveButton)
        self._username.textChanged.connect(self.enableSaveButton)
        self._passwd.textChanged.connect(self.enableSaveButton)
        self._url.textChanged.connect(self.enableSaveButton)
        self._comment.textChanged.connect(self.enableSaveButton)
        self._att_name.textChanged.connect(self.enableSaveButton)
        self._e_date_edit.dateChanged.connect(self.enableSaveButton)
        self._group.currentIndexChanged.connect(self.enableSaveButton)
        
        # never checked
        self._e_date_never.stateChanged.connect(self.enDisExpDate)
        self._e_date_never.stateChanged.connect(self.enableSaveButton)
        
        # open attachment
        self._att_button.clicked.connect(self.loadAttachment)
        
        # delete attachment
        self._att_del_button.clicked.connect(self.delAttachment)
        
        # save attachment to disk
        self._att_save_button.clicked.connect(self.saveAttachment)
        
        # attachment input label
        self._att_name.textChanged.connect(self.enableAttEditAndButton)
        
        # show/hide password
        self._show_passwd_check.stateChanged.connect(self.setVisibilityPass)
        
    def delAttachment(self):
        """
            Delete actual attachment.
        """
        logging.debug("deleting attachment")
        
        # empty attachment name and disable input
        self._att_name.clear()
        self._att_name.setDisabled(True)
        
        # empty binary data
        self._attachment_data = ""
        
        # diable del button
        self._att_del_button.setDisabled(True)
        self._att_save_button.setDisabled(True)
        
    def enableAttEditAndButton(self):
        """
            Enable attachment name input.
        """
        self._att_name.setEnabled(True)
        self._att_del_button.setEnabled(True)
        self._att_save_button.setEnabled(True)
        
    def loadGroups(self, g_id = False):
        """
            Load available groups to combobox
        """
        # set groups combobox
        group_ctrl = GroupController(self.__db_ctrl)
        
        groups = group_ctrl.selectAll()
        # tmp index
        tmp = 0
        # have to increment tmp
        inc_tmp = True
        
        # fill combobox
        for group in groups:
            logging.debug("adding group ID: %d", group._id)
            
            # load icon
            pix = QtGui.QPixmap()
            pix.loadFromData(group._icon._icon)
            
            # add item with icon, name and group ID
            self._group.addItem(QtGui.QIcon(pix), tr(group._name), group._id)
            
            if (g_id):
                # if a dont have curent group
                if (group._id != g_id and inc_tmp):
                    tmp += 1
                    
                    logging.debug("temp group index: %d, group._id: %d, g_id: %d", tmp, group._id, g_id)
                else:
                    if inc_tmp:
                        logging.debug("group found")
                        inc_tmp = False
        # set current group
        if (g_id):
            self._group.setCurrentIndex(tmp)
        
    def enDisExpDate(self, state):
        """
            Enable or disable expiration date selector. Depends on checkbox state.
            
            @param state: check box state
        """
        logging.debug("never checkbox state changed")
        if (state == QtCore.Qt.Checked):
            self._e_date_edit.setEnabled(False)
        else:
            self._e_date_edit.setEnabled(True)
        
    def enableSaveButton(self):
        """
            Enable save button.
        """
        if (not self.__save_button.isEnabled()):
            logging.debug("enabling save button")
            
            self.__save_button.setEnabled(True)
            
    def disableSaveButton(self):
        """
            Enable save button.
        """
        if (self.__save_button.isEnabled()):
            logging.debug("disabling save button")
            
            self.__save_button.setEnabled(False)
        
    def getGroupId(self):
        """
            Get group ID from combobox item.
            
            @return: group ID
        """
        index = self._group.currentIndex()
        
        # return a touple
        group_id = self._group.itemData(index).toInt()[0]
        
        logging.debug("current item index: %d group: %d", index, group_id)
        
        return group_id
        
    def keyReleaseEvent(self, event):
        """
            Handle release event.
        """
        logging.debug("key release event")
        
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
        
    def loadAttachment(self):
        """
            Exec filedialog, open file and get absolute file path and name.
        """
        home_loc = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.HomeLocation)
        file_path = QtGui.QFileDialog.getOpenFileName(self, tr("Open attachment"), home_loc)
        
        if (not file_path.isEmpty()):
            file_name = os.path.basename(str(file_path))
            
            logging.debug("attachment file path: %s", file_path)
            logging.debug("attachment file name: %s", file_name)
            
            # set attachment name
            self._att_name.setText(file_name)
            
            # read binary data
            data = self.readFile(file_path)
            
            if (data):
                self._attachment_data = data
        else:
            logging.debug("file not selected")
            
    def saveAttachment(self):
        """
            Save attachment to disk.
        """
        home_loc = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.HomeLocation)
        file_path = QtGui.QFileDialog.getSaveFileName(self, tr("Open attachment"), home_loc + os.path.sep + self._att_name.text())
        
        logging.debug("save attachment to file: %s", file_path)
        
        if (not file_path.isEmpty()):
            logging.debug("attachment file path: %s", file_path)
            
            # write data to disk
            self.writeFile(file_path)
        else:
            logging.debug("file not selected")
            
    def writeFile(self, file_path):
        """
            Write file to disk.
            
            @param file_path: file to write
        """
        try:
            f = open(file_path, "wb")
            
            f.write(self._attachment_data)
        except IOError as e:
            logging.exception(e)
            
            raise e
        except:
            logging.exception("exception writing file: %s", file_path)
            
            raise e
        finally:
            if (f):
                f.close()
            
    def readFile(self, file_path):
        """
            Read file binary. Return read data.
            
            @param file_path: path to file
            @return: on succes binary data, else None
        """
        data = None
        
        try:
            logging.debug("reading file: %s", file_path)
            f = open(file_path, "rb")
            
            data = f.read()
            
            logging.debug("file size: %i", len(data))
        except IOError as e:
            logging.exception(e)
            
            raise e
        except:
            # all other exceptions
            logging.exception("exception, file: %s", file_path)
            
            raise "exception, file: " + file_path
        finally:
            if (f):
                f.close()
            return data
        
    def saveChanges(self):
        """
            Save changes to database, read all inputs and save DB entry.
            
            @todo: implement saving password, emiting signal singalPasswdSaved, and close dialog
        """
        # TODO: implement saving password, emiting signal singalPasswdSaved, and close dialog
        pass