#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import logging
from PyQt4 import QtCore

# clipboard 'live' in miliseconds
CLIPBOARD_LIVE_MSEC = 60000

# default user name for passwords user
USER_NAME = "user"

# default data path
DATA_PATH = "data" + os.path.sep

# default settings file name
SETTINGS_FILE_NAME = "settings"

# settings file apth
SETTINGS_FILE_PATH = DATA_PATH + SETTINGS_FILE_NAME

# default DB path
DB_PATH = "db" + os.path.sep

# default DB file name
DB_FILE_NAME = "userpass.db"

# default DB
DEFAULT_DB = DB_PATH + DB_FILE_NAME

# icons path
ICONS_PATH = "icons" + os.sep

"""
    Settings keys.
"""
# database file path key
SET_KEY_DB = "database/file_path"

def writeSettings():
    """
    """
    pass
    
def readDbFilePath():
    """
        Read DB file name and path from settings file.
        
        @return: DB file path
    """
    logging.debug("reading setting file: %s", SETTINGS_FILE_PATH)
        
    # open settings
    settings = QtCore.QSettings(SETTINGS_FILE_PATH, QtCore.QSettings.NativeFormat)
    data = str(settings.value(SET_KEY_DB, DEFAULT_DB).toString())
    
    # read DB file path
    return data