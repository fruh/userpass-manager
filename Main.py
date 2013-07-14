#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from DbController import DbController
from UserController import UserController
from GroupController import GroupController
from PasswdController import PasswdController
import datetime
import time
import struct
from PyQt4 import QtGui
import sys
from MainWindow import MainWindow
import os
from LoginController import LoginController
from LoginDialog import LoginDialog

def dbTest():    
    db_con = DbController("test3.db")
    
    db_con.connectDB()
    
    user = UserController(db_con)
    group = GroupController(db_con)
    passwd_ctrl = PasswdController(db_con, "heslo")
    
    db_con.createTables()
#     user.insertUser("Ferčšo", "heslo")
    user.insertUser("Fero", "heslo")

    print(user.selectAll()[0]._passwd)
#     print(db_con.getTables())
    
    group.updateGroup(5, "nova", "description", "icon")
    passwd_ctrl.insertPassword("title", 'username', "passwd", "url", "comment", time.time(), time.time(), 1, 1, bytes(156), "attname")
    print(group.selectById(1))
    
#     passwd_ctrl.deletePassword(1)
    print(datetime.datetime.fromtimestamp(passwd_ctrl.selectAll()[0]._m_date))
    print(passwd_ctrl.selectAll()[0]._m_date)
    print(struct.unpack("<d", struct.pack("<d", time.time())))
    
    db_con._connection.close()
    
def main():
    app = QtGui.QApplication(sys.argv)
    
    db_con = DbController("test.db")
    db_con.createTables()
    
    user = UserController(db_con)
    passwd_ctrl = PasswdController(db_con, "heslo")
    
    user.insertUser("Ferčšo", "heslo")
    user.insertUser("Ferdsačšo", "heslo")
    passwd_ctrl.insertPassword("Prve heslo", 'username', "passwd", "url", "vfdfgdsg", time.time(), time.time() + 365*24*60*60, 1, 1, bytes(156), "attname", "true")
    passwd_ctrl.insertPassword("Druhe heslo", 'aaaa', "1111", "url", "commgreent", time.time(), time.time(), 2, 1, bytes(156), "attname", "false")
    passwd_ctrl.insertPassword("tretie heslo", 'bbbbb', "2222", "url", "commfwefefwent", time.time(), time.time(), 3, 1, bytes(156), "attname", "false")
    passwd_ctrl.insertPassword("stvrte heslo", 'cccc', "3333", "url", "commfewent", time.time(), time.time(), 4, 2, bytes(156), "attname", "false")
    passwd_ctrl.insertPassword("piate heslo", 'ddddd', "4444", "", "http://", time.time(), time.time(), 1, 1, bytes(156), "attname", "true")
    passwd_ctrl.insertPassword("sieste heslo", 'eeee', "5555", "url", "comfewfwefwefewmentcomfewfwefwefewmentcomfewf dsad sa sda aFEWE FDS ADwefwefewmentcomfewfwefwefewmentcomfewfwefwefewment", time.time(), time.time(), 2, 1, bytes(156), "attname", "true")
    passwd_ctrl.insertPassword("siedme heslo", 'ffff', "6666", "url", "cofewfwemment", time.time(), time.time(), 3, 1, bytes(156), "attname", "true")
    
    w = MainWindow(db_con)
    w.reloadItems()
    
    w.show()
    
    sys.exit(app.exec_())
    
def main2():
    app = QtGui.QApplication(sys.argv)
    
    db_con = DbController()
#     user = UserController(db_con)
#     
#     user.insertUser("user", "heslo")
    login_dialog = LoginDialog(db_con)

    login_dialog.show()
    
    w = MainWindow(db_con)

    login_dialog.signalSuccessfullyLogged.connect(w.setUserReloadShow)
    
    sys.exit(app.exec_())
    
if (__name__ == "__main__"):
    logging.basicConfig(format='[%(asctime)s] %(levelname)s::%(module)s::%(funcName)s() %(message)s', level=logging.DEBUG)
    
    main2()
#     dbTest()