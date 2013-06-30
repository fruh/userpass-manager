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

def dbTest():    
    db_con = DbController("test.db")
    
    db_con.connectDB()
    
    user = UserController(db_con)
    group = GroupController(db_con)
    passwd_ctrl = PasswdController(db_con, "heslo")
    
    db_con.createTables()
    user.insertUser("Ferčšo", "heslo")
#     user.insertUser("Fero", "heslo")


    print(user.selectAll()[0]._passwd)
#     print(db_con.getTables())
    
    group.updateGroup(5, "nova", "description", "icon")
    passwd_ctrl.insertPassword("title", 'username', "passwd", "url", "comment", "c_date", "e_date", 1, 1, "attachment", "attname")
    print(group.selectById(1))
    
#     passwd_ctrl.deletePassword(1)
    print(datetime.datetime.fromtimestamp(passwd_ctrl.selectAll()[0]._m_date))
    print(passwd_ctrl.selectAll()[0]._m_date)
    print(struct.unpack("<d", struct.pack("<d", time.time())))
    
    db_con._connection.close()
    
def main():
    app = QtGui.QApplication(sys.argv)
    
    db_con = DbController("test.db", "heslo")
    db_con.createTables()
    
    user = UserController(db_con)
    passwd_ctrl = PasswdController(db_con, db_con._master)
    
    user.insertUser("Ferčšo", "heslo")
    passwd_ctrl.insertPassword("Prve heslo", 'username', "passwd", "url", "vfdfgdsg", "c_date", "e_date", 1, 1, "attachment", "attname")
    passwd_ctrl.insertPassword("Prve heslo", 'username', "passwd", "url", "commgreent", "c_date", "e_date", 2, 1, "attachment", "attname")
    passwd_ctrl.insertPassword("Prve heslo", 'username', "passwd", "url", "commfwefefwent", "c_date", "e_date", 3, 1, "attachment", "attname")
    passwd_ctrl.insertPassword("Prve heslo", 'username', "passwd", "url", "commfewent", "c_date", "e_date", 4, 1, "attachment", "attname")
    passwd_ctrl.insertPassword("Prve heslo", 'username', "passwd", "url", "comewment", "c_date", "e_date", 1, 1, "attachment", "attname")
    passwd_ctrl.insertPassword("Prve heslo", 'username', "passwd", "url", "comfewfwefwefewment", "c_date", "e_date", 2, 1, "attachment", "attname")
    passwd_ctrl.insertPassword("Prve heslo", 'username', "passwd", "url", "cofewfwemment", "c_date", "e_date", 3, 1, "attachment", "attname")
    
    w = MainWindow(db_con)
    
    w.show()
    
    sys.exit(app.exec_())
    
if (__name__ == "__main__"):
    logging.basicConfig(format='[%(asctime)s] %(levelname)s::%(module)s::%(funcName)s() %(message)s', level=logging.DEBUG)
    
    main()
#     dbTest()