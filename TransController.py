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
import AppSettings
import logging

TRANSLATION = {}

def loadTranslation(lang):
    """
        Load translation from file.
    """
    f = None
    
    try:
        f = open(AppSettings.decodePath(AppSettings.TRANS_PATH + lang + AppSettings.TRANS_SUFFIX))
        
        lines = f.readlines()
        
        tmp = {}
        
        for i in range(0, len(lines) - 1):
            if (i % 2 == 0):
                # create key and value, remove last \n character and decode to utf8
                key = str(lines[i][:len(lines[i]) - 1]).decode('utf-8')
                value = str(lines[i + 1][:len(lines[i + 1]) - 1]).decode('utf-8')
                logging.debug("key: '%s', value: '%s'", key, value)
                
                tmp[key] = value
        TRANSLATION[lang] = tmp
        
    except IOError as e:
        logging.exception(e)
        
        raise e
    finally:
        if (f):
            f.close
def tr(string):
    """
        Translates word from dictionary, TRANSLATION.
        If not found in dictionary, do not translete.
        
        @param string: string to translate
        @param ignore_s: ingore shortcut char &
        
        @return: transleted string
    """
    if (not TRANSLATION.has_key(AppSettings.LANG)):
        logging.debug("translation language '%s' missing", AppSettings.LANG)
        
        return string
    
    # if we have not translation
    if not TRANSLATION[AppSettings.LANG].has_key(string):
        logging.debug("translation lang: '%s', origin: '%s', trans: missing", AppSettings.LANG, string)
        
        return string
    trans = TRANSLATION[AppSettings.LANG][string]

    logging.debug("translation lang: '%s', origin: '%s', trans: '%s'", AppSettings.LANG, string, trans)
    return trans