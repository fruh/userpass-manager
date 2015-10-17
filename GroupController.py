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
import sqlite3
import logging
from GroupModel import GroupModel

class GroupController:
    """
        Provides manipulating groups in database.
    """
    def __init__(self, db_controller):
        self._db_ctrl = db_controller
        self._connection = db_controller._connection
        self._cursor = db_controller._cursor
    
    def selectAll(self):
        """
            Select all groups from table Groups.
            @return: list of GroupModel objects
        """
        try:
            self._cursor.execute("SELECT * FROM Groups;")
            rows = self._cursor.fetchall()        
            
            logging.info("groups selected: %d", len(rows))
        except sqlite3.Error as e:
            logging.exception(e)
            
            raise e
        finally:
            groups = []
            
            for row in rows:
                groups.append(self.createGroupObj(row))
            return groups
        
    def selectById(self, g_id):
        """
            Search group by id.
            @param id: group id
            @return: row, group model object
        """
        try:
            self._cursor.execute("SELECT * FROM Groups WHERE id = :id;", {"id" : g_id})
            row = self._cursor.fetchone()
            
            if (row):
                count = 1
            else:
                count = 0
            
            logging.info("groups selected: %d", count)
        except sqlite3.Error as e:
            logging.exception(e)
            
            raise e
        finally:
            return self.createGroupObj(row)
    
    def selectByName(self, name):
        """
            Search group by name.
            @param name: group name
            @return: row
        """
        name = name.decode("utf8")
        try:
            self._cursor.execute("SELECT * FROM Groups WHERE name = :name;", {"name" : name})
            row = self._cursor.fetchone()
            
            if (row):
                count = 1
            else:
                count = 0
            logging.info("users selected: %d", count)
        except sqlite3.Error as e:
            logging.exception(e)
            
            raise e
        finally:
            return self.createGroupObj(row)

    def insertGroup(self, name, description, icon_id):
        """
            Inset group in table Groups.
            @param name: group name
            @param description: group description
            @param icon_id: group icon id
        """
        name = name.decode("utf-8")
        description = description.decode("utf-8")
        
        try:
            self._cursor.execute("INSERT INTO Groups(name, description, icon_id) VALUES(:name, :description, :icon_id)",
                                  {"name" : name, "description" : description, "icon_id" : icon_id})
            self._connection.commit()
            
            logging.info("groups with ID: %d, inserted: %d", self._cursor.lastrowid, self._cursor.rowcount)
        except sqlite3.IntegrityError as e:
            logging.warning(e)
            
            self._connection.rollback()
        except sqlite3.Error as e:
            logging.exception(e)
            
            self._connection.rollback()
            raise e
           
    def updateGroup(self, g_id, name, description, icon_id):
        """
            Updates group with id.
            @param g_id: group ID
            @param name: group name
            @param description: group description
            @param icon_id: group icon ID
        """
        name = name.decode("utf-8")
        description = description.decode("utf-8")
        
        try:
            self._cursor.execute("UPDATE Groups SET name = :name, description = :description, icon_id = :icon_id WHERE id = :id;",
                                {"id" : g_id, "name" : name, "description" : description, "icon_id" : icon_id})
            self._connection.commit()
            
            logging.info("groups updated: %d, with ID: %d", self._cursor.rowcount, g_id)
        except sqlite3.IntegrityError as e:
            logging.warning(e)
            
            self._connection.rollback()
        except sqlite3.Error as e:
            logging.exception(e)
            
            self._connection.rollback()
            raise e
            
    def deleteGroup(self, g_id):
        """
            Delete group with ID.
            @param g_id: group ID
        """
        try:
            self._cursor.execute("DELETE FROM Groups WHERE id = :g_id", {"g_id" : g_id})
            self._connection.commit()
            
            count = self._cursor.rowcount
            
            if (count > 0):
                logging.info("%d group with id: %d deleted", count, g_id)
            else:
                logging.info("%d group with id: %d found", count, g_id)
        except sqlite3.Error as e:
            logging.exception(e)
            
            self._connection.rollback()
            raise e
        
    def createGroupObj(self, dic):
        """
            Creates group from dictionary returned from db.
            
            @param dic: group returned from db
            
            @return: GroupModel object
        """
        return GroupModel(dic["id"], dic["name"], dic["description"], dic["icon_id"], self._db_ctrl)