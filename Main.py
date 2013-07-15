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
from DbController import DbController
from PyQt4 import QtGui
import sys
from MainWindow import MainWindow
import os
from LoginDialog import LoginDialog
import AppSettings
import TransController
import shutil
    
def main():
    app = QtGui.QApplication(sys.argv)
    
    logging.debug("absolute app root: '%s'", AppSettings.getAbsAppRoot())
    
    # set application icon
    app.setWindowIcon(QtGui.QIcon(AppSettings.APP_ICON_PATH))
    
    # preapare languages
    AppSettings.writeLanguage("sk")
    
    AppSettings.LANG = AppSettings.readLanguage()
    
    TransController.loadTranslation("sk")
    TransController.loadTranslation("en")
    
    # create neccessary paths if missing
    if (not os.path.exists(AppSettings.BACKUP_PATH)):
        # missing data dir
        logging.debug("creating dir: '%s'", AppSettings.BACKUP_PATH)
        
        os.makedirs(AppSettings.BACKUP_PATH)
    
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

    db_path = AppSettings.readDbFilePath()
    logging.debug("DB path: '%s'", db_path)
    
    if (not os.path.exists(db_path)):
        # if default DB file doesnt exists, run create DB dialog
        login_dialog.enLogIn(False)
    else:
        # first backup database
        backup_file = AppSettings.BACKUP_PATH + os.path.basename(db_path)
        logging.debug("backup file: '%s'", backup_file)
        
        shutil.copyfile(db_path, backup_file)

    login_dialog.show()
    w = MainWindow(db_con)
 
    # when succesfully logged load main window
    login_dialog.signalSuccessfullyLogged.connect(w.setUserReloadShow)
    
    sys.exit(app.exec_())
    
if (__name__ == "__main__"):
    logging.basicConfig(format='[%(asctime)s] %(levelname)s::%(module)s::%(funcName)s() %(message)s', level=logging.CRITICAL)
    
    main()