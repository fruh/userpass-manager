#!/usr/bin/python
# -*- coding: utf-8 -*-
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
            
            logging.info("groups selected: %i", len(rows))
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
            @return: row
        """
        try:
            self._cursor.execute("SELECT * FROM Groups WHERE id = :id;", {"id" : g_id})
            row = self._cursor.fetchone()
            
            if (row):
                count = 1
            else:
                count = 0
            
            logging.info("groups selected: %i", count)
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
            logging.info("users selected: %i", count)
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
        name = name.decode("utf8")
        description = description.decode("utf8")
        
        try:
            self._cursor.execute("INSERT INTO Groups(name, description, icon_id) VALUES(:name, :description, :icon_id)",
                                  {"name" : name, "description" : description, "icon_id" : icon_id})
            self._connection.commit()
            
            logging.info("groups with ID: %i, inserted: %i", self._cursor.lastrowid, self._cursor.rowcount)
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
        try:
            self._cursor.execute("UPDATE Groups SET name = :name, description = :description, icon_id = :icon_id WHERE id = :id;",
                                {"id" : g_id, "name" : name, "description" : description, "icon_id" : icon_id})
            self._connection.commit()
            
            logging.info("groups updated: %i, with ID: %i", self._cursor.rowcount, g_id)
        except sqlite3.IntegrityError as e:
            logging.warning(e)
            
            self._cursor.rollback()
        except sqlite3.Error as e:
            logging.exception(e)
            
            self._cursor.rollback()
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
                logging.info("%i group with id: %i deleted", count, g_id)
            else:
                logging.info("%i group with id: %i found", count, g_id)
        except sqlite3.Error as e:
            logging.exception(e)
            
            self._cursor.rollback()
            raise e
        
    def createGroupObj(self, dic):
        """
            Creates group from dictionary returned from db.
            
            @param dic: group returned from db
            
            @return: GroupModel object
        """
        return GroupModel(dic["id"], dic["name"], dic["description"], dic["icon_id"], self._db_ctrl)