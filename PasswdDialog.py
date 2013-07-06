#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from PyQt4 import QtGui, QtCore
from TransController import tr

class PasswdDialog(QtGui.QDialog):
    # emiting after saving passowrd
    # param: p_id
    signalPasswdSaved = QtCore.pyqtSignal(int)
    
    def __init__(self, db_ctrl, edit = True):
        """
            COnstructor for password dialog, displys all necessary inputs.
            
            @param db_ctrl: database controller
            @param edit: if it will we edit dialog, show creation and modification date, else do not
        """
        self.__db_ctrl = db_ctrl
        self.__edit = edit
        super(PasswdDialog, self).__init__()
        
        self.initUI()
        self.initConections()
        self.center()
        
        self._e_date_never.setChecked(True)
        
    def initUI(self):
        """
            Initilize UI components.
        """
        # not maximize, minimize buttons
        self.setWindowFlags( QtCore.Qt.Tool);
        
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
        layout_gl.addWidget(comment_label, 8 + layout_offset, 0)
        layout_gl.addWidget(group_label, 9 + layout_offset, 0)
        
        self._title = QtGui.QLineEdit()
        self._username = QtGui.QLineEdit()
        self._passwd = QtGui.QLineEdit()
        self._url = QtGui.QLineEdit()
        self._e_date = QtGui.QLineEdit()
        self._comment = QtGui.QTextEdit()
        self._comment.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)
        self._comment.setMaximumHeight(200)
        self._group = QtGui.QComboBox()
        self._att_name = QtGui.QLineEdit()
        
        layout_gl.addWidget(self._title, 0, 1)
        layout_gl.addWidget(self._username, 1, 1)
        layout_gl.addWidget(self._passwd, 2, 1)
        layout_gl.addWidget(self._url, 3, 1)
        layout_gl.addWidget(self._att_name, 7 + layout_offset, 1)
        layout_gl.addWidget(self._comment, 8 + layout_offset, 1)
        layout_gl.addWidget(self._group, 9 + layout_offset, 1)
        
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
        
        layout_gl.addWidget(self.__button_box, 10 + layout_offset, 1)
        
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
        
    def saveChanges(self):
        """
            Save changes to database, read all inputs and save DB entry.
            
            @todo: implement saving password, emiting signal singalPasswdSaved, and close dialog
        """
        # TODO: implement saving password, emiting signal singalPasswdSaved, and close dialog
        pass