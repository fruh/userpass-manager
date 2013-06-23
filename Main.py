# -*- coding: utf-8 -*-
import logging
from DbController import DbController
from UserController import UserController
from GroupController import GroupController
from PasswdController import PasswdController
import CryptoBasics

if (__name__ == "__main__"):
    logging.basicConfig(format='[%(asctime)s] %(levelname)s::%(module)s::%(funcName)s() %(message)s', level=logging.DEBUG)
    
    db_con = DbController("test.db")
    
    db_con.connectDB()
    
    user = UserController(db_con)
    group = GroupController(db_con)
    passwd_ctrl = PasswdController(db_con)
    
#     db_con.createTables()
    user.insertUser("Ferčšo", "heslo")
#     user.insertUser("Fero", "heslo")
    key = CryptoBasics.genCipherKey("ahoj", CryptoBasics.genSalt(32))
#     key = binascii.unhexlify("5ddea602fddf75ddea602fddf7765154e31016525f6cb765154e31016525f6cb")
    iv = CryptoBasics.genIV()
    #binascii.unhexlify("5ddea602fddf7765154e31016525f6cb")
    plaint = "aaaaaa"
    print(type(plaint))

    ct = CryptoBasics.encryptDataAutoPad(plaint, key, iv)
    print(ct)
    buf = CryptoBasics.decryptDataAutoPad(ct, key, iv)
    print(buf)
#     print()
#     print(CryptoBasics.genIV())
    print(user.selectAll())
#     print(db_con.getTables())
    
    group.updateGroup(5, "nova", "description", "icon")
    group.insertGroup("Default", "Default gorup")
#     passwd_ctrl.insertPassword("title", 'username', "passwd", "url", "comment", "c_date", "m_date", "e_date", "grp_id", "user_id", "attachment", "heslo")
    print(group.selectById(1))
    
    passwd_ctrl.deletePassword(1)
    print(passwd_ctrl.selectAll())
    
    db_con._connection.close()