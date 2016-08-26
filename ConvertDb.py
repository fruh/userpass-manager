#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    MIT License

    Copyright (c) 2013-2016 Frantisek Uhrecky

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
import logging
import AppSettings
import sqlite3
import os
import shutil

class ConvertDb():
    """
        Implements logic from converting database from older versions to newer, when are some changes made on DB model.
    """
    # we need dump just data, if possible
    __ENABLED_KEY_WORDS = ["INSERT"]
    __DUMP_FILE_NAME = "dump.sql"
    __DUMP_FILE_PATH = AppSettings.TMP_PATH + __DUMP_FILE_NAME
    __LINES_COUNT = 0
    
    def __init__(self, db_ctrl):
        """
            Initialize convert obejct.
            @param db_ctrl: application DB controller.
        """
        self.__db_ctrl = db_ctrl
       
    def convertDbToV1(self, old):
        """
            Convert database to version 1. Create dump, create new db, read and insert dump, set version, rewrite old DB and connect.
            
            @param old: old database
        """
        logging.info("converting database to version 1")
        
        # first create data dump from old database
        self.createDump(old)
        
        # get db name
        db_name = os.path.basename(old)
        
        # create db in tmp folder
        db_tmp = AppSettings.TMP_PATH + db_name
        logging.info("tmp db: '%s'", db_tmp)
        
        # if is in tmp dir, first remove
        if (os.path.exists(AppSettings.decodePath(db_tmp))):
            logging.info("removing from tmp dir")
            os.remove(AppSettings.decodePath(db_tmp))
            
        # connect to db and create new
        self.__db_ctrl.connectDB(db_tmp)
        self.__db_ctrl.createTables()
        
        # disable foreign key constrains
        self.__db_ctrl.enForeignKey(False)
        
        # now read dump file and insert data into new db
        fr = None
        try:
            fr = open(AppSettings.decodePath(self.__DUMP_FILE_PATH), "r")
            
            # temp line count
            tmp_count = 0.0
            # read every line
            for line in fr:
                tmp_count += 1
                
                logging.info("line: '%s'", line)
                
                self.__db_ctrl._cursor.execute(line)
                self.__db_ctrl._connection.commit()
            # now insert version
            self.__db_ctrl.insertAppDBVersion()
            
        except Exception as e:
            logging.exception(e)
            self.__db_ctrl._connection.rollback()
            
            raise e
        finally:
            if (fr):
                logging.info("closing dump file")
                fr.close()
            logging.info("removing dump file")
            os.remove(AppSettings.decodePath(self.__DUMP_FILE_PATH))
        # first disconnect from DB
        self.__db_ctrl.disconnectDB()
        
        # copy copy new db to old
        logging.info("coppying converted DB")
        shutil.copyfile(AppSettings.decodePath(db_tmp), AppSettings.decodePath(old))
        os.remove(AppSettings.decodePath(db_tmp))
        
        # reconnect to new DB
        self.__db_ctrl.connectDB(old)
        
    def createDump(self, old):
        """
            Create dump of older database. Just data dump, without tables etc.
            
            @param old: path to database
        """
        # Convert file database to SQL dump file dump.sql    
        con = sqlite3.connect(old)
        f = None
        
        try:
            f = open(AppSettings.decodePath(self.__DUMP_FILE_PATH), 'w')
            logging.info("creating data dump for database: '%s', dump file: '%s'", old, self.__DUMP_FILE_PATH)
            
            self.__LINES_COUNT = 0
            
            for line in con.iterdump():
                if (self.containsKeyWords(line)):
                    # count every line
                    self.__LINES_COUNT += 1
                    
                    f.write('%s\n' % line)
            logging.info("dump lines count: %i", self.__LINES_COUNT)
        except IOError as e:
            logging.exception(e)
            
            raise e
        finally:
            if (f):
                f.close()
            
    def containsKeyWords(self, line):
        """
            Check if the input line contains enabled key words.
            
            @param line: dump line
            @return: True on succes (contains key word), else False
        """
        for kw in self.__ENABLED_KEY_WORDS:
            if (line.find(kw) >= 0):
                logging.info("contains key word, line: '%s'", line)
                
                return True
        return False