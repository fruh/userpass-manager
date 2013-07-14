#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from DbController import DbController
from PyQt4 import QtGui
import sys
from MainWindow import MainWindow
import os
from LoginDialog import LoginDialog
import AppSettings
    
def main():
    app = QtGui.QApplication(sys.argv)
    
    # create neccessary paths if missing
    if (not os.path.exists(AppSettings.DATA_PATH)):
        # missing data dir
        logging.debug("creating dir: '%s'", AppSettings.DATA_PATH)
        
        os.makedirs(AppSettings.DATA_PATH)
        
    if (not os.path.exists(AppSettings.DB_PATH)):
        # missing db dir
        logging.debug("creating dir: '%s'", AppSettings.DB_PATH)
        
        os.makedirs(AppSettings.DB_PATH)
        
    if (not os.path.exists(AppSettings.ICONS_PATH)):
        # missing db dir
        logging.debug("creating dir: '%s'", AppSettings.ICONS_PATH)
        
        os.makedirs(AppSettings.ICONS_PATH)
    
    # DB controller instance
    db_con = DbController()
    
    # login dialog instance
    login_dialog = LoginDialog(db_con)

    if (not os.path.exists(AppSettings.readDbFilePath())):
        # id default DB file doesnt exists, run create DB dialog
        login_dialog.enLogIn(False)

    login_dialog.show()
    w = MainWindow(db_con)
 
    # when succesfully logged load main window
    login_dialog.signalSuccessfullyLogged.connect(w.setUserReloadShow)
    
    sys.exit(app.exec_())
    
if (__name__ == "__main__"):
    logging.basicConfig(format='[%(asctime)s] %(levelname)s::%(module)s::%(funcName)s() %(message)s', level=logging.CRITICAL)
    
    main()