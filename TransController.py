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
                logging.info(lines[i])
                
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