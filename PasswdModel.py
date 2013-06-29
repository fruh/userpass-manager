#!/usr/bin/python
# -*- coding: utf-8 -*-
from GroupController import GroupController
from UserController import UserController
import sqlite3
import logging

class PasswdModel:
    """
        Holds password data.
    """
    def __init__(self, p_id = None, title = None, username = None, passwd = None, 
                 url = None, comment = None, c_date = None, m_date = None, e_date = None, grp_id = None, 
                 user_id = None, attachment = None, att_name = None, salt = None, iv = None, db_ctrl = None):
        """
            Initialize PasswdModel.
            
            @param title: password title
            @param username: account username
            @param passwd: account password
            @param url: account url
            @param comment: password comment
            @param c_date: date of creation
            @param m_datedate: of modification
            @param e_date: date of expiration
            @param grp_id: password group ID, from Groups table
            @param user_id: user ID, from Users table
            @param attachment: attachment of password
            @param att_name: attachment name
            @param salt: password salt
            @param iv: input vector for cipher
            @param db_ctrl: DB controller
        """
        self._id = p_id
        self._title = title
        self._username = username
        self._passwd = passwd
        self._url = url
        self._comment = comment
        self._c_date = c_date
        self._m_date = m_date
        self._e_date = e_date
        self._grp = None
        self._user = None
        self._attachment = attachment
        self._att_name = att_name
        self._salt = salt
        self._iv = iv
        
        self._grp = self.selectGroup(grp_id, db_ctrl)
        self._user = self.selectUser(user_id, db_ctrl)
        
    def selectGroup(self, g_id, db_ctrl):
        """
            Select group from DB with id g_id.
            
            @param g_id: group ID
            @param db_ctrl: DB controller
        """
        try:
            self._grp = GroupController(db_ctrl).selectById(g_id)
        except sqlite3.Error as e:
            logging.exception("group with ID: %i, %s", g_id, e)
            
            raise e

    def selectUser(self, u_id, db_ctrl):
        """
            Select user from DB with id u_id.
            
            @param u_id: user ID
            @param db_ctrl: DB controller
        """
        try:
            self._user = UserController(db_ctrl).selectById(u_id)
        except sqlite3.Error as e:
            logging.exception("user with ID: %i, %s", u_id, e)
            
            raise e