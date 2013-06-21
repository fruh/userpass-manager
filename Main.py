# -*- coding: utf-8 -*-
import logging
from DbController import *
from UserController import *
import base64

if (__name__ == "__main__"):
    logging.basicConfig(format='[%(asctime)s] %(levelname)s::%(module)s::%(funcName)s() %(message)s', level=logging.DEBUG)
    
    db_con = DbController("test.db")
    
    db_con.connectDB()
    
    user = UserController(db_con)
#     db_con.createTables()
#     user.insertUser("Ferčšo", "heslo")
#     user.insertUser("Fero", "heslo")
    key = CryptoBasics.genCipherKey("ahoj", CryptoBasics.genSalt(32))
#     key = binascii.unhexlify("5ddea602fddf75ddea602fddf7765154e31016525f6cb765154e31016525f6cb")
    iv = CryptoBasics.genIV()
    #binascii.unhexlify("5ddea602fddf7765154e31016525f6cb")
    plaint = "sestnastznakov16sestnastznakov16aaa"
    print(type(plaint))

    ct = CryptoBasics.encryptDataAutoPad(plaint, key, iv)
    print(ct)
    buf = CryptoBasics.decryptDataAutoPad(ct, key, iv)
    print(buf)
#     print()
#     print(CryptoBasics.genIV())
    print(user.selectAll())
#     print(db_con.getTables())
    
    db_con._connection.close()