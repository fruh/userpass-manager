#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from TransController import tr
from GroupsWidget import GroupsWidget
from PasswordsWidget import PasswordsWidget
from DetailWidget import DetailWidget
from EditPasswdDialog import EditPasswdDialog

class MainWindow(QtGui.QMainWindow):
    """
        MainWindow class represents main window.
    """
    # public attr:
    _db_ctrl = None
    
    def __init__(self, db_ctrl):
        self._db_ctrl = db_ctrl
        
        super(MainWindow, self).__init__()
        
        self._close_act = None
        
        self.initUI()
        self.createActions()
        self.createMenu()
        self.initConections()
        
    def initUI(self):
        """
            Initialize gui components. Create dock widgets.
        """
#         self.resize(300, 300)
        self.setWindowTitle("UserPass Manager alpha")
        self.resize(1000, 600)
        self.center()
        
        # create main splitter, splits passwords table and gorups
        self._main_splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.setCentralWidget(self._main_splitter)
        
        # create groups widget with label, and groups
        groups_mw = QtGui.QWidget()
        groups_vl = QtGui.QVBoxLayout()
        
        groups_mw.setLayout(groups_vl)
        
        # create label
        groups_label = QtGui.QLabel("<b>" + tr("Groups") + "</b>")
        groups_vl.addWidget(groups_label)
        
        # create groups tree widget
        self._groups_tw = GroupsWidget(self)
        
        groups_vl.addWidget(self._groups_tw)

        self._main_splitter.addWidget(groups_mw)
        
        # create password central widget
        self._passwords_cw = QtGui.QWidget()
        self._main_splitter.addWidget(self._passwords_cw)
        self._main_splitter.setStretchFactor(1, 1)
        
        # create passwords layout, will contain passwords table and detail widget with spliter
        self._passwords_vl = QtGui.QVBoxLayout()
        self._passwords_cw.setLayout(self._passwords_vl)
        
        # add table widget
        self._passwords_table = PasswordsWidget(self)
        
        # create password and detail splitter
        self._passwd_splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        
        # create label
        passwdords_label = QtGui.QLabel("<b>" + tr("Passwords") + "</b>")
        self._passwords_vl.addWidget(passwdords_label)
        
        # add splitter to layout
        self._passwords_vl.addWidget(self._passwd_splitter)
        
        # create detail widget
        self._detail_w = DetailWidget(self)
        
        # add widgets to splitter
        self._passwd_splitter.addWidget(self._passwords_table)
        self._passwd_splitter.addWidget(self._detail_w)
        
        # set stretch factor for password table
        self._passwd_splitter.setStretchFactor(0, 1)
        
    def initConections(self):
        """
            Initialize all connections, handling events.
            
            @requires: initUI() first
        """
        # create connection to update table view
        self._groups_tw.signalGroupSelChanged.connect(self._passwords_table.showPasswords)
        self._groups_tw.signalGroupSelChanged.connect(self._detail_w.handleType)
        self._passwords_table.signalShowDetailPasswd.connect(self._detail_w.setPassword)
        
        # show edit passwd dialog
        self._passwords_table.signalEditPasswd.connect(self.showEditPasswdDialog)
        self._groups_tw.signalEditPasswd.connect(self.showEditPasswdDialog)
        
    def createActions(self):
        """
            Initialize all actions, i.e. Close, Save etc.
        """
        # init close
        self._close_act = QtGui.QAction(tr("&Close"), self)
        self._close_act.setShortcuts(QtGui.QKeySequence.Close)
        self._close_act.setStatusTip(tr("Close application"))
        
        # connect to slot
        self._close_act.triggered.connect(QtCore.QCoreApplication.instance().quit)
        
        # init about action
        self._about_act = QtGui.QAction(tr("About"), self)
        self._about_act.setStatusTip(tr("About UserPass Manager"))
        
        self._about_act.triggered.connect(self.aboutDialog)
        
    def createMenu(self):
        """
            Initialize menu, add actions to menu.
        """
        # create menu bar
        menubar = QtGui.QMenuBar()
        self.setMenuBar(menubar)
        
        # create menu options and add actions
        file_menu = self.menuBar().addMenu(tr("&File"))
        file_menu.addAction(self._close_act)
        
        password_menu = self.menuBar().addMenu(tr("Password"))
        
        group_menu = self.menuBar().addMenu(tr("Group"))
        
        settings_menu = self.menuBar().addMenu(tr("Settings"))
        
        about_menu = self.menuBar().addMenu(tr("About"))
        about_menu.addAction(self._about_act)
        
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
        
    def aboutDialog(self):
        QtGui.QMessageBox( QtGui.QMessageBox.Information, "About", "UserPass Manager v0.0.1 alpha\n\nSafely backup your credentials.").exec_()
        
    def showEditPasswdDialog(self, p_id):
        """
            Show edit password dialog.
            
            @param p_id: password id to edit
        """
        edit_dialog = EditPasswdDialog(self._db_ctrl, p_id)
        edit_dialog.singalPasswdSaved.connect(self.reloadItems)
        
        edit_dialog.exec_()
        
    def reloadItems(self, p_id):
        """
            Reload groups, passwords.
        """
        self._groups_tw.reloadItems()
        self._passwords_table.showAll()
        self._detail_w.setPassword(p_id)
        