#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import sqlite3
import CryptoBasics
import time
import struct

class PasswdController:
    """
        Provides manipulating passwords in database. Encrypts and decrypts data.
    """
    def __init__(self, db_controller, master):
        self._db_ctrl = db_controller
        self._connection = db_controller._connection
        self._cursor = db_controller._cursor
        self._master = master
        
        # timestamp encoding little endian and double precision
        self._TIME_PRECISION = "<d"
    
    def selectAll(self):
        """
            Select all password from table Passwords and decrypt.
            @return: rows touple of dictionaries, decrypted data
        """
        try:
            self._cursor.execute("SELECT * FROM Passwords;")
            rows = self._cursor.fetchall()
            
            # decrypt selected data
            for i in range(0, len(rows)):
                rows[i] = self.decryptRowDic(rows[i])                      
            
            logging.info("passwords selected: %i", len(rows))
        except sqlite3.Error as e:
            logging.exception(e)
            
            raise e
        finally:
            return rows
        
    def selectById(self, p_id):
        """
            Search password by id.
            @param id: password id
            @return: row
        """
        try:
            # select from table
            self._cursor.execute("SELECT * FROM Passwords WHERE id = :id;", {"id" : p_id})
            row = self._cursor.fetchone()
            
            # if exists ID
            if (row):
                count = 1
                
                # now decrypt data
                row = self.decryptRowDic(row)
            else:
                count = 0
            
            logging.info("passwords selected: %i", count)
        except sqlite3.Error as e:
            logging.exception(e)
            
            raise e
        finally:
            return row

    def insertPassword(self, title, username, passwd, url, comment, c_date, e_date, grp_id, user_id, attachment):
        """
            Inserts password in table Passwords. Encrypts inserted data. Only grp_id, user_id salt and iv are not encrypted.
            @param title: password title
            @param username: account username
            @param passwd: account password
            @param url: account url
            @param comment: password comment
            @param c_date: date of creation
            @param e_date: date of expiration
            @param grp_id: password group ID, from Groups table
            @param user_id: user ID, from Users table
            @param attachment: attachment of password
        """
        salt = unicode(CryptoBasics.genKeySalt())
        iv = CryptoBasics.genIV()
        
        # encrypt data       
        encrypted_row = self.encryptAndPrepRow(title, username, passwd, url, 
                                               comment, c_date, e_date, 
                                               grp_id, user_id, attachment, 
                                               salt, iv)
        
        try:
            self._cursor.execute("""INSERT INTO 
                Passwords(title, username, passwd, url, comment, c_date, m_date, e_date, grp_id, user_id, attachment, salt, iv)
                VALUES(:title, :username, :passwd, :url, :comment, :c_date, :m_date, :e_date, :grp_id, :user_id, :attachment, :salt, :iv)""",
                                  encrypted_row)
            self._connection.commit()
            
            logging.info("passwords with ID: %i, inserted: %i", self._cursor.lastrowid, self._cursor.rowcount)
        except sqlite3.IntegrityError as e:
            logging.warning(e)
            
            self._cursor.rollback()
        except sqlite3.Error as e:
            logging.exception(e)
            
            self._cursor.rollback()
            raise e
            
    def updatePasswd(self, p_id, title, username, passwd, url, comment, c_date, e_date, grp_id, user_id, attachment):
        """
            Updates password in table Passwords. Encrypts inserted data. Only grp_id, user_id salt and iv are not encrypted.
            @param title: password title
            @param username: account username
            @param passwd: account password
            @param url: account url
            @param comment: password comment
            @param c_date: date of creation
            @param e_date: date of expiration
            @param grp_id: password group ID, from Groups table
            @param user_id: user ID, from Users table
            @param attachment: attachment of password
        """
        try:
            # first select old row to get salt and iv
            old = self.selectById(p_id)
            
            # if old row exists
            if old:
                # encrypt data and prepare for sqlite
                row = self.encryptAndPrepRow(title, username, passwd, url, comment, c_date, e_date, grp_id, user_id, attachment, old["salt"], old["iv"])
                
                self._cursor.execute("""UPDATE Passwords SET title = :title, username = :username, passwd = :passwd, url = :url, 
                                    comment = :comment, c_date = :c_date, m_date = :m_date, e_date = :e_date, grp_id = :grp_id,
                                    attachment = :attachment WHERE id = :id;""", row)
                self._connection.commit()
                
                logging.debug("passwd with ID: %i updated.", p_id)
            else:
                logging.warning("password with id: %i doesn't exists. Can't be updated.", p_id)
        except sqlite3.IntegrityError as e:
            logging.warning(e)
            
            self._cursor.rollback()
        except sqlite3.Error as e:
            logging.exception(e)
            
            self._cursor.rollback()
            raise e
          
    def updatePasswdDic(self, row):
        """
            Updates password record, implements updatePasswd().
            
            @param row: new data
        """
        self.updatePasswd(row["p_id"], row["title"], row["username"], row["passwd"], row["url"], row["comment"], 
                        row["c_date"], row["e_date"], row["grp_id"], row["user_id"], row["attachment"])
        
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
            
            self._cursor.rollback()
            raise e
            
    def encryptAndPrepRow(self, title, username, passwd, url, comment, c_date, e_date, grp_id, user_id, attachment, salt, iv):
        """
            Encrypts password in table Passwords. Encrypts inserted data. Only grp_id, user_id salt and iv are not encrypted.
            Also change m_date column, modification date, to current timestamp. Encrypted data are inserted as BLOB type.
            
            And prepares them for sqlite binary data.
            @param title: password title
            @param username: account username
            @param passwd: account password
            @param url: account url
            @param comment: password comment
            @param c_date: date of creation
            @param e_date: date of expiration
            @param grp_id: password group ID, from Groups table
            @param user_id: user ID, from Users table
            @param attachment: attachment of password
            @param salt: secret key salt
            @param iv: cipher input vector
            
            @return: encrypted dictionary data
        """
        secret_key = CryptoBasics.genCipherKey(self._master, salt)
        
        # pack time (float) to bytes, need to encrypt it, add padding
        m_date = time.time()
        logging.debug("modification timestamp: %f", m_date)
        
        # use little endian and float type to convert timestamp
        m_date = struct.pack(self._TIME_PRECISION, m_date)

        # encrypt data
        title = CryptoBasics.encryptDataAutoPad(title, secret_key, iv)
        username = CryptoBasics.encryptDataAutoPad(username, secret_key, iv)
        passwd = CryptoBasics.encryptDataAutoPad(passwd, secret_key, iv)
        url = CryptoBasics.encryptDataAutoPad(url, secret_key, iv)
        comment = CryptoBasics.encryptDataAutoPad(comment, secret_key, iv)
        c_date = CryptoBasics.encryptDataAutoPad(c_date, secret_key, iv)
        m_date = CryptoBasics.encryptDataAutoPad(m_date, secret_key, iv)
        e_date = CryptoBasics.encryptDataAutoPad(e_date, secret_key, iv)
        attachment = CryptoBasics.encryptDataAutoPad(attachment, secret_key, iv)
        
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
        
        return {"title" : title, "username" : username, "passwd" : passwd, "url" : url, "comment" : comment, 
            "c_date" : c_date, "m_date" : m_date, "e_date" : e_date, "grp_id" : grp_id, "user_id" : user_id,
            "attachment" : attachment, "salt" : salt, "iv" : iv}
    
    def decryptRow(self, p_id, title, username, passwd, url, comment, c_date, m_date, e_date, grp_id, user_id, attachment, salt, iv):
        """
            Decrypts password in table Passwords. Decrypts slected data. Only grp_id, user_id salt and iv are not encrypted.
            
            @param p_id: password id
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
            @param salt: secret key salt
            @param iv: cipher input vector
            
            @return: enrypted dictionary data
        """
        secret_key = CryptoBasics.genCipherKey(self._master, salt)
        
        # decrypt data
        title = CryptoBasics.decryptDataAutoPad(title, secret_key, iv)
        username = CryptoBasics.decryptDataAutoPad(username, secret_key, iv)
        passwd = CryptoBasics.decryptDataAutoPad(passwd, secret_key, iv)
        url = CryptoBasics.decryptDataAutoPad(url, secret_key, iv)
        comment = CryptoBasics.decryptDataAutoPad(comment, secret_key, iv)
        c_date = CryptoBasics.decryptDataAutoPad(c_date, secret_key, iv)
        
        # unpack returns a touple, but I need just one value
        m_date = struct.unpack(self._TIME_PRECISION, CryptoBasics.decryptDataAutoPad(m_date, secret_key, iv))[0]
        
        e_date = CryptoBasics.decryptDataAutoPad(e_date, secret_key, iv)
        attachment = CryptoBasics.decryptDataAutoPad(attachment, secret_key, iv)
        
        return {"id" : id, "title" : title, "username" : username, "passwd" : passwd, "url" : url, "comment" : comment, 
            "c_date" : c_date, "m_date" : m_date, "e_date" : e_date, "grp_id" : grp_id, "user_id" : user_id,
            "attachment" : attachment, "salt" : salt, "iv" : iv}
        
    def decryptRowDic(self, row):
        """
            Decrypts password in table Passwords. Decrypts slected data. Only grp_id, user_id salt and iv are not encrypted.
            
            @param row: selected row, encrypted, as dictionary
            
            @return: enrypted dictionary data
        """
        return self.decryptRow(row["id"], row["title"], row["username"], row["passwd"], row["url"], row["comment"],
                            row["c_date"], row["m_date"], row["e_date"], row["grp_id"], row["user_id"], 
                            row["attachment"], row["salt"], row["iv"])
        
    def setMaster(self, master):
        """
            Set master password for controller.
            
            @param master: master password
        """
        self._master = master
        
    def getMster(self):
        """
            Returns currnet master password.
            
            @return: master
        """
        return self._master