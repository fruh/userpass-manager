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
SETTINGS_FILE_NAME = "settings.ini"

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
    # open settings
    settings = QtCore.QSettings(SETTINGS_FILE_PATH, QtCore.QSettings.IniFormat)
    data = str(settings.value(SET_KEY_DB, DEFAULT_DB).toString())
    
    logging.debug("reading setting file: '%s', key: '%s', data: '%s'", SETTINGS_FILE_PATH, SET_KEY_DB, data)
    
    # read DB file path
    return data

def writeDbFilePath(db_path):
    """
        Write DB file name and path to settings file. Write just relative path.
        
        @param db_path: DB file path
    """
    rel_path = os.path.relpath(db_path, os.getcwd())
    
    logging.debug("current working dir: '%s'", os.getcwd())
    logging.debug("abs. path: '%s', rel. path: '%s'", db_path, rel_path)
    logging.debug("writing setting file: '%s', key: '%s', data: '%s'", SETTINGS_FILE_PATH, SET_KEY_DB, rel_path)
        
    # open settings
    settings = QtCore.QSettings(SETTINGS_FILE_PATH, QtCore.QSettings.IniFormat)
    settings.setValue(SET_KEY_DB, rel_path)