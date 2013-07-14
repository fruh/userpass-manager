#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from TransController import tr
import logging
from LoginController import LoginController
import AppSettings

class LoginDialog(QtGui.QDialog):
    """
        Login dialog window, serves login user, and create new user.
    """
    # emmitted signal, when successfuly logged user
    # first param is user name, and second master password
    signalSuccessfullyLogged = QtCore.pyqtSignal(str, str)
    
    def __init__(self, db_ctrl):
        self.__db_ctrl = db_ctrl
        
        super(LoginDialog, self).__init__()
        
        self.initUI()
        self.center()
        self.initConnections()
        
    def initUI(self):
        """
            Initialize UI components.
        """
        self.setWindowTitle(tr("Log In"))
        self.setFixedWidth(500)
        
        # not maximize, minimize buttons
        self.setWindowFlags(QtCore.Qt.Tool);
        
        # create main grid layout
        layout_gl = QtGui.QGridLayout()
        self.setLayout(layout_gl)
        
        # labels
#         username_label = QtGui.QLabel("<b>" + tr("Username:") + "</b>")
        passwd_label = QtGui.QLabel("<b>" + tr("Password:") + "</b>")
        
        # add to layout
#         layout_gl.addWidget(username_label, 0, 0)
        layout_gl.addWidget(passwd_label, 0, 0)
        
#         self._username = QtGui.QLineEdit()
#         layout_gl.addWidget(self._username, 0, 1)
        
        self._passwd = QtGui.QLineEdit()
        
        # hide password
        self._passwd.setEchoMode(QtGui.QLineEdit.Password)
        
        # password layout
        passwd_hl = QtGui.QHBoxLayout()
        
        # add password edit line to layout
        passwd_hl.addWidget(self._passwd)
        
        # password visibility check box
        self._show_passwd_check = QtGui.QCheckBox(tr("Show"))
        self._show_passwd_check.setChecked(False)
        passwd_hl.addWidget(self._show_passwd_check)
        
        layout_gl.addLayout(passwd_hl, 0, 1)
        
        # create buttons
        self._button_box = QtGui.QDialogButtonBox()
        
        self.__login_button = QtGui.QPushButton(tr("&Log In"))
        self.__login_button.setEnabled(False)
        
        self.__close_button = QtGui.QPushButton(tr("&Close"))
        
        self._button_box.addButton(self.__login_button, QtGui.QDialogButtonBox.AcceptRole)
        self._button_box.addButton(self.__close_button, QtGui.QDialogButtonBox.RejectRole)
        
        layout_gl.addWidget(self._button_box, 1, 1)
        
        # db button box
        self._db_button_box = QtGui.QDialogButtonBox()
    
        self.__open_db = QtGui.QPushButton(tr("Open Database"))
        self.__create_db = QtGui.QPushButton(tr("Create Database"))
        
    def initConnections(self):
        """
            Init connections, reaction on signals.
        """
        # show/hide password
        self._show_passwd_check.stateChanged.connect(self.setVisibilityPass)
        
        # enable loggin button
#         self._username.textChanged.connect(self.enableLogInButton)
        self._passwd.textChanged.connect(self.enableLogInButton)
        
        # button connections
        self._button_box.rejected.connect(QtGui.QApplication.exit)
        self._button_box.accepted.connect(self.logIn)
        
    def logIn(self):
        """
            Read input lines and login user if possible.
        """
        logging.debug("logging user ...")
        
        self.__db_ctrl.connectDB(AppSettings.readDbFilePath())
        login_ctrl = LoginController(self.__db_ctrl)
        
        username = AppSettings.USER_NAME
        master = str(self._passwd.text()).decode('utf-8')
        
        logged_user = login_ctrl.logInUser(username, master)
        
        if (logged_user):
            self.signalSuccessfullyLogged.emit(username, master)
            
            self.close()
        
    def setVisibilityPass(self, state):
        """
            Set visibility password, depends on checkbox.
        """
        if (state == QtCore.Qt.Checked):
            self._passwd.setEchoMode(QtGui.QLineEdit.Normal)
        else:
            self._passwd.setEchoMode(QtGui.QLineEdit.Password)
        
    def enableLogInButton(self):
        """
            Enable login button. If is empty one of username or password, then disable.
        """
        if (self._passwd.text().isEmpty()):
            if (self.__login_button.isEnabled()):
                logging.debug("disabling login button")
                
                self.__login_button.setEnabled(False)
        else:
            if (not self.__login_button.isEnabled()):
                logging.debug("enabling login button")
                
                self.__login_button.setEnabled(True)
        
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