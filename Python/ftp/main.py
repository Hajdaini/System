#coding:utf-8

import ftp
from getpass import getpass

# Donnees de connexion par defaut
state = "idle"
address = "127.0.0.1"
user = ""
password = ""
port="21"
tmp = ""

# connecteur
while state != "connected":
    if state == "error":
        print("\nFTP failed to connect: {}".format(res))

    tmp = input("FTP Host ({}): ".format(address))
    address = tmp if tmp != "" else address

    tmp = input("FTP User ({}): ".format(user))
    user = tmp if tmp != "" else user

    tmp = getpass("FTP Password: ")
    password = tmp if tmp != "" else password

    tmp = input("FTP Port ({}): ".format(port))
    port = tmp if tmp != "" else port

    state, res = ftp.connect(address, user, password, port)

# Interpreteur
ftp.interpreter(res, address, user)
