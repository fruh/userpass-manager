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
