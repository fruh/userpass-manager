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
from GroupController import GroupController
from IconController import IconController
import os
import AppSettings
from ConvertDb import ConvertDb
import InfoMsgBoxes
from TransController import tr

class DbController:
    """
        Implements basic DB initialitation.
    """
    def __init__(self, database = None):
        """
            If DB file is specified, then create DB, and tables if did not exist.
        """
        self._cursor = None
        self._database = database
        self._connection = None
        
        # whether DB file existed
        self._existed = False
        
        if (database):
            self.connectDB()
            
            if (not self._existed):
                self.createTables()
        
    def connectDB(self, database = None):
        """
            Connect existing or creates new database
            @param database: db file path with name
        """
        try:
            self.disconnectDB()
            
            if (database):
                self._database = database
            logging.info("database: '%s'", self._database)
                
            # check if file exists    
            self._existed = os.path.exists(self._database)
            
            with sqlite3.connect(self._database) as self._connection:
                # turn on dictionary mode
                self._connection.row_factory = sqlite3.Row
                self._cursor = self._connection.cursor()
            logging.info("'%s' successfully opened.", self._database)
            logging.info("SQLite version %s", self.getDBVersion())
            
            # if is old, check for conversion
            if (self._existed):
                # check version 
                logging.info("App DB version %s", self.getAppDBVersion())
                
                self.checkVersion()
            
            self.enForeignKey()
        except sqlite3.Error as e:
            logging.exception(e)
            raise e
    
    def checkVersion(self):
        """
            Check opened database version, if neccessaary and posible, then convert to current.
        """
        version = self.getAppDBVersion()
        
        if ((version == False) or (version < AppSettings.APP_DB_VERSION)):
            # need to be converted
            logging.info("need to convert from version: '%s'", version)
            converter = ConvertDb(self)
            
            converter.convertDbToV1(self._database)
            
            InfoMsgBoxes.showInfoMsg(tr("Database successfully converted to new version."))
    
    def disconnectDB(self):
        """
            Disconnect connected database.
        """
        if (self._connection):
            logging.info("disconnecting DB: '%s'", self._database)
            
            self._connection.close()
            del self._connection
            self._connection = None
            
    
    def getDBVersion(self):
        """ 
            Returns SQLite version 
        """
        self._cursor.execute('SELECT SQLITE_VERSION()')
    
        return self._cursor.fetchone()[0]
    
    def getAppDBVersion(self):
        """
            Return current connected database application vesrion.
        """
        if (self._connection):
            try:
                self._cursor.execute("SELECT version FROM Version;")
                
                row = self._cursor.fetchone()
                
                if (row):
                    return int(row["version"])
                return False
            except sqlite3.Error as e:
                logging.exception(e)
                
                return False
        logging.info("not connected to DB")
        return False
    
    def createTables(self):      
        """
            Creates neccessery tables. Contains foreign key constrains.
            
            Users table: users of UserPass manager application.
            Icons table: contains icons for groups
            Groups table: groups of passwords i.e. (Page, SSH, E-Mail, PC and user defined)
            Password table: holds usernames, passwords and their metada in ecrypted form
        """ 
        try:
            self._cursor.executescript("""
                DROP TABLE IF EXISTS Users;
                CREATE TABLE Users(id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, 
                    passwd TEXT NOT NULL, salt_p TEXT NOT NULL);
                
                DROP TABLE IF EXISTS Icons;
                CREATE TABLE Icons(id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, icon BLOB);
                
                DROP TABLE IF EXISTS Version;
                CREATE TABLE Version(id INTEGER PRIMARY KEY, version INTEGER UNIQUE NOT NULL);
                
                DROP TABLE IF EXISTS Groups;
                CREATE TABLE Groups(id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, 
                    description TEXT, 
                    icon_id INTEGER DEFAULT 0 REFERENCES Icons(id) ON DELETE SET DEFAULT);
                
                DROP TABLE IF EXISTS Passwords;
                CREATE TABLE Passwords(id INTEGER PRIMARY KEY, title BLOB NOT NULL, username BLOB NOT NULL,
                    passwd BLOB NOT NULL, url BLOB, comment BLOB, 
                    c_date BLOB NOT NULL, m_date BLOB NOT NULL, e_date BLOB NOT NULL,
                    grp_id INTEGER REFERENCES Groups(id) ON DELETE CASCADE, 
                    user_id INTEGER REFERENCES Users(id) ON DELETE CASCADE, 
                    attachment BLOB, att_name BLOB,
                    salt TEXT, iv BLOB, expire TEXT);
                """)
            self._connection.commit()
            
            logging.info("%i tables created.", self._cursor.rowcount)
        except sqlite3.Error as e:
            logging.exception(e)
            
            # rollback changes
            self._connection.rollback()
            raise e
    
    def insertDefRows(self):
        """
            Insert default values to rows.
        """
        # insert default icons
        self.insertDefaultIcons()
        
        # insert default groups
        self.insertDefaultGroups()
        
        # insert App DB version
        self.insertAppDBVersion()
    
    def insertAppDBVersion(self):
        """
            Insert into DB app version DB.
        """
        try:
            self._cursor.execute("INSERT INTO Version(version) VALUES(:version)",
                                  {"version" : AppSettings.APP_DB_VERSION})
            self._connection.commit()
            
            logging.info("Version with ID: %d, inserted: %s", self._cursor.lastrowid, AppSettings.APP_DB_VERSION)
        except sqlite3.IntegrityError as e:
            logging.warning(e)
            
            self._connection.rollback()
        except sqlite3.Error as e:
            logging.exception(e)
            
            self._connection.rollback()
            raise e
    
    def insertDefaultIcons(self):
        """
            Creates default icons for groups.
            Page, SSH, E-Mail, PC, Code Revision, UserPass icon
        """
        icon_ctrl = IconController(self)
        
        icon_ctrl.insertIcon("key-personal", AppSettings.ICONS_PATH + "key-personal.ico")
        icon_ctrl.insertIcon("key-ssh", AppSettings.ICONS_PATH+ "key-ssh.ico")
        icon_ctrl.insertIcon("key", AppSettings.ICONS_PATH + "key.ico")
        icon_ctrl.insertIcon("person", AppSettings.ICONS_PATH + "person.ico")
        icon_ctrl.insertIcon("git", AppSettings.ICONS_PATH + "git.ico")
        icon_ctrl.insertIcon("bank", AppSettings.ICONS_PATH + "bank.ico")
        icon_ctrl.insertIcon("userpass", AppSettings.ICONS_PATH + "userpass.ico")
        
    def insertDefaultGroups(self):
        """
            Creates default password groups.
            Page, SSH, E-Mail, PC, Code Revision
        """
        grp_ctrl = GroupController(self)
        icon_ctrl = IconController(self)
        
        # now insert new groups
        grp_ctrl.insertGroup("Page", "Web page credentials.", icon_ctrl.selectByName("key-personal")._id)
        grp_ctrl.insertGroup("SSH", "SSH credentials.", icon_ctrl.selectByName("key-ssh")._id)
        grp_ctrl.insertGroup("E-Mail", "E-Mail credentials.", icon_ctrl.selectByName("key")._id)
        grp_ctrl.insertGroup("PC", "PC credentials.", icon_ctrl.selectByName("person")._id)
        grp_ctrl.insertGroup("Code revision", "Code revision credentials.", icon_ctrl.selectByName("git")._id)
        grp_ctrl.insertGroup("Bank account", "Bank account credentials.", icon_ctrl.selectByName("bank")._id)
    
    def getTables(self):
        self._cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        
        return self._cursor.fetchall()
    
    def enForeignKey(self, b = True):
        """
            Enable/disable foreign key. Default disbaled. On every connection need to enable foreign keys.
            
            @param b: booleane parameter, enable true, disable false
        """
        try:
            if (b):
                logging.info("Enabling foreign keys.")
                
                self._cursor.execute("PRAGMA foreign_keys = ON;")
            else:
                logging.info("Disabling foreign keys.")
                
                self._cursor.execute("PRAGMA foreign_keys = OFF;")
            self._connection.commit()
        except sqlite3.Error as e:
            logging.exception(e)
            
            # rollback changes
            self._connection.rollback()
            raise e
        