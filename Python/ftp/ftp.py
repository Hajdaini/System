#coding:utf-8

import ftplib
import os
import re
import importlib

# Donnees de connexion par defaut
state = "idle"
address = "127.0.0.1"
user = "nobody"
password = ""
port="21"
tmp = ""


def connect(address="127.0.0.1", user="", password="", port="21"):
        try:
            ftp = ftplib.FTP(address, user, password)
            # ftp.connect(address, int(port))
            return ("connected", ftp)
        except ftplib.all_errors as e:
            return ("failed", e)


def is_dir(ftp_handle, name):
    r1 = re.findall(r"type=(file|dir)", ftp_handle.sendcmd('MLST {}'.format(name)))
    type = ''.join(r1)
    return type == "dir"


def create_parent_dir(fpath):
    dirname = os.path.dirname(fpath)
    while not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
            print("created directory : {0}".format(dirname))
        except:
            create_parent_dir(dirname)


def download_file(ftp_handle, name, dest, overwrite):
    create_parent_dir(dest.lstrip("/"))
    if not os.path.exists(dest) or overwrite is True:
        try:
            with open(dest, 'wb') as f:
                ftp_handle.retrbinary("RETR {0}".format(name), f.write)
            print("Downloaded: {0}".format(dest))
        except FileNotFoundError:
            print("FAILED: {0}".format(dest))
    else:
        print("Already exists: {0}".format(dest))


def mirror_dir(ftp_handle, name, overwrite):
    for item in ftp_handle.nlst(name):
        if is_ftp_dir(ftp_handle, item): # if it is a directory then we don't care
            mirror_ftp_dir(ftp_handle, item, overwrite)
        else:
            download_ftp_file(ftp_handle, item, item, overwrite)


def download_tree(ftp_handle, path, overwrite=False):
    path = path.lstrip("/")
    original_directory = os.getcwd()
    mirror_ftp_dir(ftp_handle, path, overwrite)
    os.chdir(original_directory)


def interpreter(ftp, address="", user=""):
    while True:
        command = input("ftp://{}@{}:{} > ".format(user, address, ftp.pwd()))
        if command == "":
            continue
        command = command.split()

        try:
            cmd = importlib.import_module("commands.{}".format(command[0]))
            cls = getattr(cmd, command[0])
            cls = cls(command, ftp, address, user)
            cls.call()
            ftp = cls.ftp
        except:
            print('command {} not found. Type help to see available commands'. format(command[0]))
        if command[0] == "exit":
            break

# connecteur
while state != "connected":
    if state == "error":
        print("\nFTP failed to connect: {}".format(res))

    tmp = input("FTP Host ({}): ".format(address))
    address = tmp if tmp != "" else address

    tmp = input("FTP User ({}): ".format(user))
    user = tmp if tmp != "" else user

    tmp = input("FTP Password: ")
    password = tmp if tmp != "" else password

    tmp = input("FTP Port ({}): ".format(port))
    port = tmp if tmp != "" else port

    state, res = connect(address, user, password, port)

# Interpreteur
interpreter(res, address, user)
