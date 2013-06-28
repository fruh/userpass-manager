#!/usr/bin/python
# -*- coding: utf-8 -*-

LANG = "sk"

TRANSLATION = {"sk" : 
               {"hello" : "ahoj"},
               "en" :
               {"hello" : "Hello"}}

def tr(string, ignore_s = False):
    """
        Translates word from dictionary, TRANSLATION and also set shortcut char position.
        If not found in dictionary, do not translete.
        
        @param string: string to translate
        @param ignore_s: ingore shortcut char &
        
        @return: transleted string
    """
    # remove shortcut char &
    tmp = string.replace("&", "")
#     print(tmp)
    # if we have not translation
    if not TRANSLATION[LANG].has_key(tmp):
        return string
    
    # ignore shorcut char &
    if not ignore_s:
        # find possiotion
        pos = string.find("&")
    
        # if contains shorcut char
        if (pos != -1):
            tran_len = len(TRANSLATION[LANG][tmp])
            
            # if position of shortcut char is lower then length could be same position
            if (pos < tran_len):
                return TRANSLATION[LANG][tmp][:pos] + "&" + TRANSLATION[LANG][tmp][pos:]
            else:
                return "&" + TRANSLATION[LANG][tmp]
    
    return TRANSLATION[LANG][tmp]