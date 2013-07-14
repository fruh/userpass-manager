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