#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

class UserModel:
    """
        Holds User data.
    """
    def __init__(self, u_id = None, name = None, passwd = None, salt = None, master = None):
        """
            Initialize UserModel.
            
            @param u_id: user id
            @param name: user name
            @param passwd: user passwd hash
            @param salt: password salt
            @param master: master password, plain text
        """
        self._id = u_id
        self._name = name
        self._passwd = passwd
        self._salt = salt
        self._master = master