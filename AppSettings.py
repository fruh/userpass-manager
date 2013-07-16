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
import os
import logging
from PyQt4 import QtCore
import sys

# file ssytem encoding
FILE_SYS_ENCODING = sys.getfilesystemencoding()

def getAbsAppRoot():
    """
        Return absolute root dir.
    """
    
    root_dir = os.path.dirname((str(sys.argv[0]).decode(FILE_SYS_ENCODING)).encode("utf-8"))
    
    if (len(root_dir) > 0):
        # if is not empty add dir separator at the end
        root_dir = root_dir + os.sep
    
    return str(root_dir)

# application relative path path
APP_REL_ROOT = getAbsAppRoot()

# App version
APP_VERSION = "v0.0.4-alpha"

# language
LANG = "en"

# clipboard 'live' in miliseconds
CLIPBOARD_LIVE_MSEC = 60000

# default user name for passwords user
USER_NAME = "user"

# default data path
DATA_PATH = APP_REL_ROOT + "data" + os.path.sep

# default settings file name
SETTINGS_FILE_NAME = "settings.ini"

# settings file apth
SETTINGS_FILE_PATH = DATA_PATH + SETTINGS_FILE_NAME

# default DB path
DB_PATH = APP_REL_ROOT + "db" + os.path.sep

# default DB file name
DB_FILE_NAME = "userpass.db"

# default DB
DEFAULT_DB = "db" + os.path.sep + DB_FILE_NAME

# icons path
ICONS_PATH = APP_REL_ROOT + "icons" + os.sep

# translations path
TRANS_PATH = APP_REL_ROOT + "translation" + os.sep

# translation suffix
TRANS_SUFFIX = ".txt"

# backup path
BACKUP_PATH = APP_REL_ROOT + "backup" + os.sep

# app icon path
APP_ICON_PATH = ICONS_PATH + "userpass.ico"

"""
    Settings keys.
"""
# database file path key
SET_KEY_DB = "database/file_path"

# language key
SET_KEY_LANG = "general/language"

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
    settings = QtCore.QSettings(QtCore.QString.fromUtf8(SETTINGS_FILE_PATH), QtCore.QSettings.IniFormat)
    data = str(settings.value(SET_KEY_DB, DEFAULT_DB).toString().toUtf8())
    
    logging.debug("reading setting file: '%s', key: '%s', data: '%s'", SETTINGS_FILE_PATH, SET_KEY_DB, data)
    
    # read DB file path
    return APP_REL_ROOT + data

def writeDbFilePath(db_path):
    """
        Write DB file name and path to settings file. Write just relative path from App root dir.
        
        @param db_path: DB file path
    """
    rel_path = str(os.path.relpath(db_path, APP_REL_ROOT))
    
    logging.debug("current working dir: '%s'", APP_REL_ROOT)
    logging.debug("abs. path: '%s', rel. path: '%s'", db_path, rel_path)
    logging.debug("writing setting file: '%s', key: '%s', data: '%s'", SETTINGS_FILE_PATH, SET_KEY_DB, rel_path)
        
    # open settings
    settings = QtCore.QSettings(QtCore.QString.fromUtf8(SETTINGS_FILE_PATH), QtCore.QSettings.IniFormat)
    settings.setValue(SET_KEY_DB, QtCore.QString.fromUtf8(rel_path))
    
def readLanguage():
    """
        Read default language
        
        @return: language
    """
    # open settings
    settings = QtCore.QSettings(QtCore.QString.fromUtf8(SETTINGS_FILE_PATH), QtCore.QSettings.IniFormat)
    data = str(settings.value(SET_KEY_LANG, LANG).toString().toUtf8())
    
    logging.debug("reading setting file: '%s', key: '%s', data: '%s'", SETTINGS_FILE_PATH, SET_KEY_LANG, data) 
    
    # read DB file path
    return data

def writeLanguage(lang):
    """
        Write language.
        
        @param lang: language mark
    """
    logging.debug("writing setting file: '%s', key: '%s', data: '%s'", SETTINGS_FILE_PATH, SET_KEY_LANG, lang)
        
    # open settings
    settings = QtCore.QSettings(QtCore.QString.fromUtf8(SETTINGS_FILE_PATH), QtCore.QSettings.IniFormat)
    settings.setValue(SET_KEY_LANG, QtCore.QString.fromUtf8(lang))
    
def decodePath(path):
    """
        Decode path from utf-8 to system encoding.
        
        @param path: path in utf-8 encoding
        
        @return: encoded path in system encoding
    """
    out = str(path).decode("utf-8").encode(FILE_SYS_ENCODING)
    
    logging.info("in: '%s', out: '%s'", path, out)
    
    return out