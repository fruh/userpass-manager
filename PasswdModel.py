#!/usr/bin/python
# -*- coding: utf-8 -*-
class PasswdModel:
    """
        Holds password data.
    """
    def __init__(self, p_id = None, title = None, username = None, passwd = None, 
                 url = None, comment = None, c_date = None, m_date = None, e_date = None, grp_id = None, 
                 user_id = None, attachment = None, salt = None, iv = None):
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
            @param salt: password salt
            @param iv: input vector for cipher
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
        self._grp_id = grp_id
        self._user_id = user_id
        self._attachment = attachment
        self._salt = salt
        self._iv = iv