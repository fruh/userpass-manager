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
    global FILE_SYS_ENCODING
    
    if (not FILE_SYS_ENCODING):
        FILE_SYS_ENCODING = "utf-8"
    root_dir = os.path.dirname((str(sys.argv[0]).decode(FILE_SYS_ENCODING)).encode("utf-8"))
    
    if (len(root_dir) > 0):
        # if is not empty add dir separator at the end
        root_dir = root_dir + os.sep
    
    return str(root_dir)

# application relative path path
APP_ABS_ROOT = getAbsAppRoot()

# tmp directory
TMP_PATH = APP_ABS_ROOT + "tmp" + os.sep

# App version
APP_VERSION = "v0.0.6-alpha"

# App version
APP_DB_VERSION = 1

# language
LANG = "en"

# when inserted worng password, sleep for seconds
WRONG_PASWD_SLEEP = 3

# clipboard 'live' in miliseconds
CLIPBOARD_LIVE_MSEC = 60000

# default user name for passwords user
USER_NAME = "user"

# default data path
DATA_PATH = APP_ABS_ROOT + "data" + os.path.sep

# default settings file name
SETTINGS_FILE_NAME = "settings.ini"

# settings file apth
SETTINGS_FILE_PATH = DATA_PATH + SETTINGS_FILE_NAME

# default DB path
DB_PATH = APP_ABS_ROOT + "db" + os.path.sep

# default DB file name
DB_FILE_NAME = "userpass.db"

# default DB
DEFAULT_DB = "db" + os.path.sep + DB_FILE_NAME

# icons path
ICONS_PATH = APP_ABS_ROOT + "icons" + os.sep

# translations path
TRANS_PATH = APP_ABS_ROOT + "translation" + os.sep

# translation suffix
TRANS_SUFFIX = ".txt"

# backup path
BACKUP_PATH = APP_ABS_ROOT + "backup" + os.sep

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
    return data

def writeDbFilePath(db_path):
    """
        Write DB file name and path to settings file. Write just relative path from App root dir.
        
        @param db_path: DB file path
    """
    logging.debug("current working dir: '%s'", APP_ABS_ROOT)
    logging.debug("writing setting file: '%s', key: '%s', data: '%s'", SETTINGS_FILE_PATH, SET_KEY_DB, db_path)
        
    # open settings
    settings = QtCore.QSettings(QtCore.QString.fromUtf8(SETTINGS_FILE_PATH), QtCore.QSettings.IniFormat)
    settings.setValue(SET_KEY_DB, QtCore.QString.fromUtf8(db_path))
    
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