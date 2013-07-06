#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import sqlite3
import CryptoBasics
import time
import struct
from PasswdModel import PasswdModel
from TransController import tr

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
            
            logging.info("passwords selected: %d", len(rows))
        except sqlite3.Error as e:
            logging.exception(e)
            
            raise e
        finally:
            passwords = []
            
            for row in rows:
                passwords.append(self.createPasswdObj(row))
            return passwords
        
    def selectById(self, p_id):
        """
            Search password by id.
            @paramp_id: password id
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
            
            logging.info("passwords selected: %d", count)
        except sqlite3.Error as e:
            logging.exception(e)
            
            raise e
        finally:
            return [self.createPasswdObj(row)]
        
    def selectByGroupId(self, g_id):
        """
            Search password by group id.
            @param g_id: group id
            @return: rows
        """
        try:
            # select from table
            self._cursor.execute("SELECT * FROM Passwords WHERE grp_id = :id;", {"id" : g_id})
            rows = self._cursor.fetchall()
            
            # decrypt selected data
            for i in range(0, len(rows)):
                rows[i] = self.decryptRowDic(rows[i])                      
            
            logging.info("passwords selected: %d", len(rows))
        except sqlite3.Error as e:
            logging.exception(e)
            
            raise e
        finally:
            passwords = []
            
            for row in rows:
                passwords.append(self.createPasswdObj(row))
            return passwords

    def insertPassword(self, title, username, passwd, url, comment, c_date, e_date, grp_id, user_id, attachment, att_name, expire):
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
            @param att_name: attachment name
            @param expire: if password expires, should be set to 'true' string
        """
        salt = CryptoBasics.genKeySalt().decode("utf8")
        iv = CryptoBasics.genIV()
        
        # encrypt data       
        encrypted_row = self.encryptAndPrepRow(title, username, passwd, url, 
                                               comment, c_date, e_date, 
                                               grp_id, user_id, attachment,
                                               att_name, 
                                               salt, iv, expire)
        
        try:
            self._cursor.execute("""INSERT INTO 
                Passwords(title, username, passwd, url, comment, c_date, m_date, e_date, grp_id, user_id, attachment, att_name, salt, iv, expire)
                VALUES(:title, :username, :passwd, :url, :comment, :c_date, :m_date, :e_date, :grp_id, :user_id, :attachment, :att_name, 
                :salt, :iv, :expire)""",
                                  encrypted_row)
            self._connection.commit()
            
            logging.info("passwords with ID: %d, inserted: %d", self._cursor.lastrowid, self._cursor.rowcount)
        except sqlite3.IntegrityError as e:
            logging.warning(e)
            
            self._connection.rollback()
        except sqlite3.Error as e:
            logging.exception(e)
            
            self._connection.rollback()
            raise e
            
    def updatePasswd(self, p_id, title, username, passwd, url, comment, e_date, grp_id, user_id, attachment, att_name, expire):
        """
            Updates password in table Passwords. Encrypts inserted data. Only grp_id, user_id salt and iv are not encrypted.
            @param title: password title
            @param username: account username
            @param passwd: account password
            @param url: account url
            @param comment: password comment
            @param e_date: date of expiration
            @param grp_id: password group ID, from Groups table
            @param user_id: user ID, from Users table
            @param attachment: attachment of password
            @param att_name: attachment name
            @param expire: if password expires, should be set to 'true' string
        """
        try:
            # first select old row to get salt and iv
            old = self.selectById(p_id)[0]
            
            # if old row exists
            if old:
                # encrypt data and prepare for sqlite
                # creation date doesnt matter, cant be changed
                row = self.encryptAndPrepRow(title, username, passwd, url, comment, old._c_date, 
                                             e_date, grp_id, user_id, attachment, att_name, old._salt, old._iv, expire)
                
                # add password ID to row
                row["id"] = p_id
                
                self._cursor.execute("""UPDATE Passwords SET title = :title, username = :username, passwd = :passwd, url = :url, 
                                    comment = :comment, m_date = :m_date, e_date = :e_date, grp_id = :grp_id,
                                    attachment = :attachment, att_name = :att_name, expire = :expire WHERE id = :id;""", row)
                self._connection.commit()
                
                logging.debug("passwd with ID: %d updated.", p_id)
            else:
                logging.warning("password with id: %d doesn't exists. Can't be updated.", p_id)
        except sqlite3.IntegrityError as e:
            logging.warning(e)
            
            self._connection.rollback()
        except sqlite3.Error as e:
            logging.exception(e)
            
            self._connection.rollback()
            raise e
          
    def updatePasswdDic(self, row):
        """
            Updates password record, implements updatePasswd().
            
            @param row: new data
        """
        self.updatePasswd(row["p_id"], row["title"], row["username"], row["passwd"], row["url"], row["comment"], 
                        row["e_date"], row["grp_id"], row["user_id"], row["attachment"], row["att_name"], row["expire"])
        
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
                logging.info("%d password with id: %d deleted", count, p_id)
            else:
                logging.info("%d password with id: %d found", count, p_id)
        except sqlite3.Error as e:
            logging.exception(e)
            
            self._connection.rollback()
            raise e
            
    def encryptAndPrepRow(self, title, username, passwd, url, comment, c_date, e_date, grp_id, user_id, attachment, att_name, salt, iv, expire):
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
            @param att_name: attachment name
            @param salt: secret key salt
            @param iv: cipher input vector
            @param expire: if password expires, should be set to 'true' string
            
            @return: encrypted dictionary data
        """
        secret_key = CryptoBasics.genCipherKey(self._master, salt)
        
        # pack time (float) to bytes, need to encrypt it, add padding
        m_date = time.time()
        logging.debug("modification timestamp: %f", m_date)
        
        # use little endian and float type to convert timestamp
        c_date = struct.pack(self._TIME_PRECISION, c_date)
        e_date = struct.pack(self._TIME_PRECISION, e_date)
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
        att_name = CryptoBasics.encryptDataAutoPad(att_name, secret_key, iv)
        expire = CryptoBasics.encryptDataAutoPad(expire, secret_key, iv)
        
        # prepare binary data
        title = sqlite3.Binary(title)
        username = sqlite3.Binary(username)
        passwd = sqlite3.Binary(passwd)
        url = sqlite3.Binary(url)
        comment = sqlite3.Binary(comment)
        c_date = sqlite3.Binary(c_date)
        m_date = sqlite3.Binary(m_date)
        e_date = sqlite3.Binary(e_date)
#         grp_id = sqlite3.Binary(grp_id)
#         user_id = sqlite3.Binary(user_id)
        attachment = sqlite3.Binary(attachment)
        att_name = sqlite3.Binary(att_name)
        iv = sqlite3.Binary(iv)
        expire = sqlite3.Binary(expire)
        
        return {'title' : title, 'username' : username, 'passwd' : passwd, 'url' : url, 'comment' : comment, 
            'c_date' : c_date, 'm_date' : m_date, 'e_date' : e_date, 'grp_id' : grp_id, 'user_id' : user_id,
            'attachment' : attachment, 'att_name' : att_name, 'salt' : salt, 'iv' : iv, 'expire' : expire}
    
    def decryptRow(self, p_id, title, username, passwd, url, comment, c_date, m_date, e_date, grp_id, user_id, attachment, att_name, salt, iv, expire):
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
            @param att_name: attachment name
            @param salt: secret key salt
            @param iv: cipher input vector
            @param expire: if password expires, should be set to 'true' string
            
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
        e_date = CryptoBasics.decryptDataAutoPad(e_date, secret_key, iv)
        m_date = CryptoBasics.decryptDataAutoPad(m_date, secret_key, iv)
        
        
        # unpack returns a touple, but I need just one value
        m_date = struct.unpack(self._TIME_PRECISION, m_date)[0]
        c_date = struct.unpack(self._TIME_PRECISION, c_date)[0]
        e_date = struct.unpack(self._TIME_PRECISION, e_date)[0]
      
        attachment = CryptoBasics.decryptDataAutoPad(attachment, secret_key, iv)
        att_name = CryptoBasics.decryptDataAutoPad(att_name, secret_key, iv)
        expire = CryptoBasics.decryptDataAutoPad(expire, secret_key, iv)
        
        return {"id" :p_id, "title" : title, "username" : username, "passwd" : passwd, "url" : url, "comment" : comment, 
            "c_date" : c_date, "m_date" : m_date, "e_date" : e_date, "grp_id" : grp_id, "user_id" : user_id,
            "attachment" : attachment, "att_name" : att_name, "salt" : salt, "iv" : iv, "expire" : expire}
        
    def decryptRowDic(self, row):
        """
            Decrypts password in table Passwords. Decrypts slected data. Only grp_id, user_id salt and iv are not encrypted.
            
            @param row: selected row, encrypted, as dictionary
            
            @return: enrypted dictionary data
        """
        return self.decryptRow(row["id"], row["title"], row["username"], row["passwd"], row["url"], row["comment"],
                            row["c_date"], row["m_date"], row["e_date"], row["grp_id"], row["user_id"], 
                            row["attachment"], row["att_name"], row["salt"], row["iv"], row["expire"])
    
    def createPasswdObj(self, dic):
        """
            Creates group from dictionary returned from db.
            
            @param dic: group returned from db
            
            @return: GroupModel object
        """
        return PasswdModel(dic["id"], dic["title"], dic["username"], dic["passwd"], dic["url"], dic["comment"],
                            dic["c_date"], dic["m_date"], dic["e_date"], dic["grp_id"], dic["user_id"], 
                            dic["attachment"], dic["att_name"], dic["salt"], dic["iv"], dic["expire"], self._db_ctrl)
        
    @staticmethod
    def getVisibleColumns():
        """
            Return visible table columns.
            
            @return: list of column names
        """
        return [tr("Title"), tr("Username"), tr("Password"), tr("Url"), tr("Comment"), 
                tr("C. Date"), tr("M. Date"), tr("E. Date"), tr("Group"), tr("Att. Name"), tr("Expire")]
        
    @staticmethod
    def getTableColumns():
        """
            Return minimum table columns.
            
            @return: list of column names
        """
        return [tr("Title"), tr("Username"), tr("Password"), tr("Url")]