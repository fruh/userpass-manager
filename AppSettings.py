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

# language
LANG = "en"

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

# translations path
TRANS_PATH = "translation" + os.sep

# translation suffix
TRANS_SUFFIX = ".txt"

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
    
def readLanguage():
    """
        Read default language
        
        @return: language
    """
    # open settings
    settings = QtCore.QSettings(SETTINGS_FILE_PATH, QtCore.QSettings.IniFormat)
    data = str(settings.value(SET_KEY_LANG, LANG).toString())
    
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
    settings = QtCore.QSettings(SETTINGS_FILE_PATH, QtCore.QSettings.IniFormat)
    settings.setValue(SET_KEY_LANG, lang)