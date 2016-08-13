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
    
def ifNotExCreate(directory):
    """
        If does not exists dir, create it.
        
        @param directory: directory to check and create
    """
    if (not os.path.exists(AppSettings.decodePath(directory))):
        # missing data dir
        logging.info("creating dir: '%s'", directory)
        
        os.makedirs(AppSettings.decodePath(directory))
    
def main():
    app = QtGui.QApplication(sys.argv)
    
    logging.info("Absolute app root: '%s'", AppSettings.APP_ABS_ROOT)
    
    # set application icon
    app.setWindowIcon(QtGui.QIcon(AppSettings.APP_ICON_PATH))
    
    # create neccessary paths if missing
    ifNotExCreate(AppSettings.TMP_PATH)
    ifNotExCreate(AppSettings.BACKUP_PATH)
    ifNotExCreate(AppSettings.DATA_PATH)
    ifNotExCreate(AppSettings.DB_PATH)
    ifNotExCreate(AppSettings.ICONS_PATH)
    
    # preapare languages
    AppSettings.writeLanguage("sk")
    
    AppSettings.LANG = AppSettings.readLanguage()
    
    TransController.loadTranslation("sk")
    TransController.loadTranslation("en")
    
    # DB controller instance
    db_con = DbController()

    # login dialog instance
    login_dialog = LoginDialog(db_con)

    db_path = AppSettings.readDbFilePath()
    logging.info("DB path: '%s'", db_path)
    
    if (not os.path.exists(AppSettings.decodePath(db_path))):
        # if default DB file doesnt exists, run create DB dialog
        login_dialog.enLogIn(False)
    else:
        # first backup database
        backup_file = AppSettings.BACKUP_PATH + os.path.basename(db_path)
        logging.info("backup file: '%s'", backup_file)
        
        shutil.copyfile(AppSettings.decodePath(db_path), AppSettings.decodePath(backup_file))

    login_dialog.show()
    w = MainWindow(db_con)
 
    # when succesfully logged load main window
    login_dialog.signalSuccessfullyLogged.connect(w.setUserReloadShow)
    
    sys.exit(app.exec_())
    
if (__name__ == "__main__"):
    logging.basicConfig(format='[%(asctime)s] %(levelname)s::%(module)s::%(funcName)s() %(message)s', level=logging.WARNING)
    
    main()
