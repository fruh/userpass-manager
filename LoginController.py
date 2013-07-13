#!/usr/bin/python
# -*- coding: utf-8 -*-
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