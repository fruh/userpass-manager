#!/usr/bin/python
# -*- coding: utf-8 -*-

LANG = "sk"

TRANSLATION = {"sk" : 
               {"hello" : "ahoj"},
               "en" :
               {"hello" : "Hello"}}

def tr(string):
    """
        Translates word from dictionary, TRANSLATION.
        If not found in dictionary, do not translete.
        
        @param string: string to translate
        @param ignore_s: ingore shortcut char &
        
        @return: transleted string
    """
    # if we have not translation
    if not TRANSLATION[LANG].has_key(string):
        return string

    return TRANSLATION[LANG][string]