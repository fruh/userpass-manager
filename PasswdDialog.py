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
from PyQt4 import QtGui, QtCore
from TransController import tr
from GroupController import GroupController
import os
import AppSettings
from SaveDialog import SaveDialog
import InfoMsgBoxes

class PasswdDialog(SaveDialog):
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
        
        self.initUi()
        self.initConections()
        self.center()
        
        # dafult never expire password
        self._e_date_never.setChecked(True)
        
        # intialize variables
        self._attachment_data = ""
        
    def initUi(self):
        """
            Initilize UI components.
        """
        SaveDialog.initUi(self)

        title_label = QtGui.QLabel("<b>" + tr("Title:") + "</b>")
        username_label = QtGui.QLabel("<b>" + tr("Username:") + "</b>")
        passwd_label = QtGui.QLabel("<b>" + tr("Password:") + "</b>")
        url_label = QtGui.QLabel("<b>" + tr("URL:")  + "</b>")
        
        if (self.__edit):
            # if it is edit dialog display
            layout_offset = 0
            
            c_date_label = QtGui.QLabel("<b>" + tr("Creation date:") + "</b>")
            m_date_label = QtGui.QLabel("<b>" + tr("Modification date:") + "</b>")
            
            self._layout_gl.addWidget(c_date_label, 4, 0)
            self._layout_gl.addWidget(m_date_label, 5, 0)
            
            self._c_date = QtGui.QLabel()
            self._m_date = QtGui.QLabel()
            
            self._layout_gl.addWidget(self._c_date, 4, 1)
            self._layout_gl.addWidget(self._m_date, 5, 1)
        else:
            layout_offset = -2
            
        e_date_label = QtGui.QLabel("<b>" + tr("Expiration date:") + "</b>")
        comment_label = QtGui.QLabel("<b>" + tr("Comment:") + "</b>")
        attachment_label = QtGui.QLabel("<b>" + tr("Attachment:") + "</b>")
        group_label = QtGui.QLabel("<b>" + tr("Groups:") + "</b>")
        
        self._layout_gl.addWidget(title_label, 0, 0)
        self._layout_gl.addWidget(username_label, 1, 0)
        self._layout_gl.addWidget(passwd_label, 2, 0)
        self._layout_gl.addWidget(url_label, 3, 0)
        self._layout_gl.addWidget(e_date_label, 6 + layout_offset, 0)
        self._layout_gl.addWidget(attachment_label, 7 + layout_offset, 0)
        self._layout_gl.addWidget(comment_label, 9 + layout_offset, 0)
        self._layout_gl.addWidget(group_label, 10 + layout_offset, 0)
        
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
        self._comment.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self._comment.setMaximumHeight(200)
        self._group = QtGui.QComboBox()
        self._att_name = QtGui.QLineEdit()
        self._att_name.setEnabled(False)
        
        self._layout_gl.addWidget(self._title, 0, 1)
        self._layout_gl.addWidget(self._username, 1, 1)
        self._layout_gl.addLayout(passwd_hl, 2, 1)
        self._layout_gl.addWidget(self._url, 3, 1)
        
        # attachment vertical layout
        att_vl = QtGui.QVBoxLayout()
        
        # attachment layout
        att_hl_1 = QtGui.QHBoxLayout()
        att_hl_2 = QtGui.QHBoxLayout()
        
        att_vl.addLayout(att_hl_1)
        att_vl.addLayout(att_hl_2)
        
        # open file button
        self._att_button = QtGui.QPushButton(tr("Load"))
        self._att_del_button = QtGui.QPushButton(tr("Delete"))
        self._att_save_button = QtGui.QPushButton(tr("Download"))
        self._att_open_button = QtGui.QPushButton(tr("Open"))
        
        self._att_del_button.setEnabled(False)
        self._att_save_button.setEnabled(False)
        self._att_open_button.setEnabled(False)
        
        att_hl_1.addWidget(self._att_button)
        att_hl_1.addWidget(self._att_del_button)
        att_hl_2.addWidget(self._att_save_button)
        att_hl_2.addWidget(self._att_open_button)
        
        self._layout_gl.addWidget(self._att_name, 7 + layout_offset, 1)
        self._layout_gl.addLayout(att_vl, 8 + layout_offset, 1)
        self._layout_gl.addWidget(self._comment, 9 + layout_offset, 1)
        self._layout_gl.addWidget(self._group, 10 + layout_offset, 1)
        
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
        self._layout_gl.addLayout(e_date_hl, 6 + layout_offset, 1)
        
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
        SaveDialog.initConections(self)
        
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
        
        # open attachment file
        self._att_open_button.clicked.connect(self.openAttachment)
        
        # attachment input label
        self._att_name.textChanged.connect(self.enableAttEditAndButton)
        
        # show/hide password
        self._show_passwd_check.stateChanged.connect(self.setVisibilityPass)
        
    def delAttachment(self):
        """
            Delete actual attachment.
        """
        logging.info("deleting attachment")
        
        # empty attachment name and disable input
        self._att_name.clear()
        self._att_name.setDisabled(True)
        
        # empty binary data
        self._attachment_data = ""
        
        # diable del button
        self._att_del_button.setDisabled(True)
        self._att_save_button.setDisabled(True)
        self._att_open_button.setDisabled(True)
        
    def enableAttEditAndButton(self):
        """
            Enable attachment name input.
        """
        self._att_name.setEnabled(True)
        self._att_del_button.setEnabled(True)
        self._att_save_button.setEnabled(True)
        self._att_open_button.setEnabled(True)
        
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
            logging.info("adding group ID: %d", group._id)
            
            # load icon
            pix = QtGui.QPixmap()
            pix.loadFromData(group._icon._icon)
            
            # add item with icon, name and group ID
            self._group.addItem(QtGui.QIcon(pix), tr(group._name), group._id)
            
            if (g_id):
                # if a dont have curent group
                if (group._id != g_id and inc_tmp):
                    tmp += 1
                    
                    logging.info("temp group index: %d, group._id: %d, g_id: %d", tmp, group._id, g_id)
                else:
                    if inc_tmp:
                        logging.info("group found")
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
        
    def getGroupId(self):
        """
            Get group ID from combobox item.
            
            @return: group ID
        """
        index = self._group.currentIndex()
        
        # return a touple
        group_id = self._group.itemData(index).toInt()[0]
        
        logging.info("current item index: %d group: %d", index, group_id)
        
        return group_id
        
    def keyReleaseEvent(self, event):
        """
            Handle release event.
        """
        logging.info("key release event")
        
    def loadAttachment(self):
        """
            Exec filedialog, open file and get absolute file path and name.
        """
        try:
            home_loc = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.HomeLocation)
            file_path = QtGui.QFileDialog.getOpenFileName(self, tr("Open attachment"), home_loc)
            
            if (not file_path.isEmpty()):
                file_path = str(file_path.toUtf8())
                file_name = os.path.basename(file_path)
                
                logging.info("attachment file path: %s", file_path)
                logging.info("attachment file name: %s", file_name)
                
                # set attachment name
                self._att_name.setText(QtCore.QString.fromUtf8(file_name))
                
                # read binary data
                data = self.readFile(file_path)
                
                if (data):
                    self._attachment_data = data
                    self.enableSaveButton()
            else:
                logging.debug("file not selected")
        except Exception as e:
            logging.exception(e)
            
            InfoMsgBoxes.showErrorMsg(e)
            
    def saveAttachment(self):
        """
            Save attachment to disk.
        """
        try:
            home_loc = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.HomeLocation)
            home_loc = QtCore.QString.fromUtf8(home_loc + os.path.sep)
            home_loc.append(self._att_name.text())
            file_path = QtGui.QFileDialog.getSaveFileName(self, tr("Open attachment"), home_loc)
            
            logging.info("save attachment to file: %s", file_path)
            
            if (not file_path.isEmpty()):
                file_path = str(file_path.toUtf8())
                logging.info("attachment file path: %s", file_path)
                
                # write data to disk
                self.writeFile(file_path)
            else:
                logging.info("file not selected")
        except Exception as e:
            logging.exception(e)
            
            InfoMsgBoxes.showErrorMsg(e)
            
    def openAttachment(self):
        """
            Open attachment using desktop services.
        """
        try:
            tmp_file = AppSettings.TMP_PATH + str(self._att_name.text().toUtf8())
            logging.info("saving attachment to tmp file: '%s'", tmp_file)
            
            self.writeFile(tmp_file)
            
            if (not QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(QtCore.QString.fromUtf8(tmp_file)))):
                # not succesfully opened
                QtGui.QMessageBox(QtGui.QMessageBox.Information, tr("Something wrong!"), tr("Can't open file '") + QtCore.QString.fromUtf8(tmp_file) + "\n" + 
                                  tr("Save it to disk and open with selected program.")).exec_()
        except Exception as e:
            logging.exception(e)
            
            InfoMsgBoxes.showErrorMsg(e)
            
    def writeFile(self, file_path):
        """
            Write file to disk.
            
            @param file_path: file to write
        """
        f = None
        try:
            f = open(AppSettings.decodePath(file_path), "wb")
            
            f.write(self._attachment_data)
        except IOError as e:
            logging.exception(e)
            
            raise e
        except:
            logging.exception("exception writting file: %s", file_path)
            
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
        f = None
        
        try:
            logging.info("reading file: %s", file_path)
            f = open(AppSettings.decodePath(file_path), "rb")
            
            data = f.read()
            
            logging.info("file size: %i", len(data))
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