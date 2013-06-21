#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import sqlite3
import CryptoBasics

class PasswdController:
    """
        Provides manipulating passwords in database.
    """
    def __init__(self, db_controller):
        self._db_ctrl = db_controller
        self._connection = db_controller._connection
        self._cursor = db_controller._cursor
    
    def selectAll(self):
        """
            Select all password from table Passwords.
            @return: rows touple of dictionaries
        """
        try:
            self._cursor.execute("SELECT * FROM Passwords;")
            rows = self._cursor.fetchall()        
            
            logging.info("passwords selected: %i", len(rows))
        except sqlite3.Error as e:
            logging.exception(e)
        finally:
            return rows
        
    def selectById(self, p_id):
        """
            Search password by id.
            @param id: password id
            @return: row
        """
        try:
            self._cursor.execute("SELECT * FROM Passwords WHERE id = :id;", {"id" : p_id})
            row = self._cursor.fetchone()
            
            if (row):
                count = 1
            else:
                count = 0
            
            logging.info("passwords selected: %i", count)
        except sqlite3.Error as e:
            logging.exception(e)
        finally:
            return row

    def insertPassword(self, title, username, passwd, url, comment, c_date, m_date, e_date, grp_id, user_id, attachment):
        """
            Inserts password in table Passwords. Encrypts inserted data. Only grp_id, user_id salt and iv are not encrypted.
            @param title: password title
            @param username: account username
            @param passwd: account password
            @param url: account url
            @param comment: password comment
            @param c_date: date of creation
            @param m_date: date of modification
            @param e_date: date of expiration
            @param grp_id: password group ID, from Groups table
            @param user_id: user ID, from Users table
            @param attachment: attachment of password
        """
        salt = unicode(CryptoBasics.genKeySalt())
        iv = CryptoBasics.genIV()
        
        # prepare binary data
        title = sqlite3.Binary(title)
        username = sqlite3.Binary(username)
        passwd = sqlite3.Binary(passwd)
        url = sqlite3.Binary(url)
        comment = sqlite3.Binary(comment)
        c_date = sqlite3.Binary(c_date)
        m_date = sqlite3.Binary(m_date)
        e_date = sqlite3.Binary(e_date)
        grp_id = sqlite3.Binary(grp_id)
        user_id = sqlite3.Binary(user_id)
        attachment = sqlite3.Binary(attachment)
        iv = sqlite3.Binary(iv)
        
        try:
            self._cursor.execute("""INSERT INTO 
                Passwords(title, username, passwd, url, comment, c_date, m_date, e_date, grp_id, user_id, attachment, salt, iv)
                VALUES(:title, :username, :passwd, :url, :comment, :c_date, :m_date, :e_date, :grp_id, :user_id, :attachment, :salt, :iv)""",
                                  {"title" : title, "username" : username, "passwd" : passwd, "url" : url, "comment" : comment, 
                                   "c_date" : c_date, "m_date" : m_date, "e_date" : e_date, "grp_id" : grp_id, "user_id" : user_id,
                                   "attachment" : attachment, "salt" : salt, "iv" : iv})
            self._connection.commit()
            logging.info("passwords inserted: %i", self._cursor.rowcount)
        except sqlite3.IntegrityError as e:
            logging.warning(e)
        except sqlite3.Error as e:
            logging.exception(e)
            
    def deletePassword(self, p_id):
        """
            Delete password with ID.
            @param p_id: password ID
        """
        try:
            self._cursor.execute("DELETE FROM Passwords WHERE id = :id", {"id" : p_id})
            self._connection.commit()
            
            count = self._cursor.rowcount
            
            if (count > 0):
                logging.info("%i password with id: %i deleted", count, p_id)
            else:
                logging.info("%i password with id: %i found", count, p_id)
        except sqlite3.Error as e:
            logging.exception(e)