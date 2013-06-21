#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import logging

class DbController:
    """
        Implements basic DB initialitation.
    """
    def __init__(self, database = None):
        self._cursor = None
        self._database = database
        self._connection = None
        
    def connectDB(self, database = None):
        """
            Connect existing or creates new database
            @param database: db file path with name
        """
        try:
            if (database):
                self._database = database
            with sqlite3.connect(self._database) as self._connection:
                # turn on dictionary mode
                self._connection.row_factory = sqlite3.Row
                self._cursor = self._connection.cursor()
            logging.info("'%s' successfully opened.", self._database)
            logging.info("SQLite version %s", self.getDBVersion())
        except sqlite3.Error as e:
            logging.exception(e)
            raise e
    
    def getDBVersion(self):
        """ Returns SQLite version """
        self._cursor.execute('SELECT SQLITE_VERSION()')
    
        return self._cursor.fetchone()[0]
    
    def createTables(self):      
        """
            Creates neccessery tables.
        """ 
        try:
            self._cursor.executescript("""
                DROP TABLE IF EXISTS Users;
                CREATE TABLE Users(id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, 
                    passwd TEXT NOT NULL, salt_p TEXT NOT NULL);
                
                DROP TABLE IF EXISTS Groups;
                CREATE TABLE Groups(id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, 
                    description TEXT, icon BLOB);
                
                DROP TABLE IF EXISTS Passwords;
                CREATE TABLE Passwords(id INTEGER PRIMARY KEY, title BLOB NOT NULL, username BLOB NOT NULL,
                    passwd BLOB NOT NULL, url BLOB, comment BLOB, 
                    c_date BLOB NOT NULL, m_date BLOB NOT NULL, BLOB DATETIME,
                    grp_id INTEGER, user_id INTEGER, attachment BLOB,
                    salt TEXT, iv TEXT,
                    FOREIGN KEY(grp_id) REFERENCES Groups(id),
                    FOREIGN KEY(user_id) REFERENCES Users(id));
                """)
            self._connection.commit()
            logging.info("tables created.")
        except sqlite3.Error as e:
            logging.exception(e)
            
            self._connection.rollback()
    
    def getTables(self):
        self._cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        
        return self._cursor.fetchall()
    
if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s] %(levelname)s::%(module)s::%(funcName)s() %(message)s', level=logging.INFO)
    
    db = DbController()
    
    db.connectDB("test.db")