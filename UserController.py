#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import logging
import CryptoBasics
from UserModel import UserModel

class UserController:
    """
        Provides manipulating users in database. Provides password hashing with salt.
    """
    def __init__(self, db_controller):
        self._db_ctrl = db_controller
        self._connection = db_controller._connection
        self._cursor = db_controller._cursor
    
    def selectAll(self):
        """
            Select all users from table Users.
            @return: list of users (UserModel)
        """
        try:
            self._cursor.execute("SELECT * FROM Users;")
            rows = self._cursor.fetchall()        
            
            logging.info("users selected: %s", len(rows))
        except sqlite3.Error as e:
            logging.exception(e)
            
            raise e
        finally:
            users = []
            
            for row in rows:
                users.append(self.createUserObj(row))
            return users
        
    def selectById(self, u_id):
        """
            Search user by id.
            @param id: user id
            @return: UserModel object
        """
        try:
            self._cursor.execute("SELECT * FROM Users WHERE id = :id;", {"id" : u_id})
            row = self._cursor.fetchone()
            
            if (row):
                count = 1
            else:
                count = 0
            
            logging.info("users selected: %s", count)
        except sqlite3.Error as e:
            logging.exception(e)
            
            raise e
        finally:
            return self.createUserObj(row)
    
    def selectByName(self, name):
        """
            Search user by name.
            @param name: user name
            @return: UserModel object, other None
        """
        name = name.decode('utf-8')
        try:
            self._cursor.execute("SELECT * FROM Users WHERE name = :name;", {"name" : name})
            row = self._cursor.fetchone()
            
            if (row):
                count = 1
            else:
                count = 0
            logging.info("users selected: %s", count)
        except sqlite3.Error as e:
            logging.exception(e)
            
            raise e
        finally:
            return self.createUserObj(row)

    def selectByNameMaster(self, name, master):
        """
            Select user from database by username and password.
            
            @param name: username
            @param master: plain text password
            
            @return: UserModel object, or None
        """
        name = name.decode('utf-8')
        master = master.decode('utf-8')
        user = None
        try:
            user = self.selectByName(name)
            
            if (not user):
                logging.debug("username doesn't exist, %s", name)
                
                return None
            
            # prepare hash
            passwd = user._salt + master
            passwd = CryptoBasics.getSha512(passwd)
        except sqlite3.Error as e:
            logging.exception(e)
            
            raise e
        finally:
            if (user and user._passwd == passwd):
                logging.debug("user with username '%s' selected", name)
                
                user._master = master
                
                return user
            else:
                logging.debug("user password not correct, '%s'", master)
                
                return None

    def insertUser(self, name, passwd):
        """
            Inset user in talbe Users. User password is hashed with salt_p.
            @param name: user name
            @param passwd: user password
        """
        name = name.decode('utf-8')
        passwd = passwd.decode('utf-8')
        # generate salt using cryptographic safe pseudo-random generator
        salt_p = CryptoBasics.genUserPassSalt()
        
        # prepends salts and create hash
        passwd = salt_p + passwd
        passwd = CryptoBasics.getSha512(passwd)
        
        try:
            self._cursor.execute("INSERT INTO Users(name, passwd, salt_p) VALUES(:name, :passwd, :salt_p)",
                                  {"name" : name, "passwd" : passwd, "salt_p" : salt_p})
            self._connection.commit()
            logging.info("users with ID: %i, inserted: %s", self._cursor.lastrowid, self._cursor.rowcount)
        except sqlite3.IntegrityError as e:
            logging.warning(e)
        except sqlite3.Error as e:
            logging.exception(e)
            
            self._connection.rollback()
            raise e
            
    def deleteUser(self, u_id):
        """
            Delete user with ID.
            @param u_id: user ID
        """
        try:
            self._cursor.execute("DELETE FROM Users WHERE id = :u_id", {"u_id" : u_id})
            self._connection.commit()
            
            count = self._cursor.rowcount
            
            if (count > 0):
                logging.info("%s user with id: %s deleted", count, u_id)
            else:
                logging.info("%s user with id: %s found", count, u_id)
        except sqlite3.Error as e:
            logging.exception(e)
            
            self._connection.rollback()
            raise e
        
    def createUserObj(self, dic):
        """
            Creates user from dictionary returned from db.
            
            @param dic: user returned from db
            
            @return: UserModel object, or None
        """
        user = None
        try:
            user = UserModel(dic["id"], dic["name"], dic["passwd"], dic["salt_p"])
        except Exception as e:
            logging.exception(e)
        finally:
            return user