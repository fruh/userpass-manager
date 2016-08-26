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
import logging
from UserController import UserController

class LoginController:
    """
        Log in master user.
    """
    def __init__(self, db_ctrl):
        """
            @param db_ctrl: Database controller
        """
        self.__db_ctrl = db_ctrl
        
    def logInUser(self, username, master):
        """
            Login user with username and master password.
            
            @param username: username
            @param master: master password
            
            @return: on succes user object, other False
        """
        user_ctrl = UserController(self.__db_ctrl)
        
        user = user_ctrl.selectByNameMaster(username, master)
        
        if (user):
            logging.debug("user logged in")
            
            return user
        else:
            logging.debug("user NOT logged in")
            
            return False