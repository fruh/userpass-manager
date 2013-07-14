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