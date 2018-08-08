#coding:utf-8

#--------------------------------------
# Imports
#--------------------------------------
import ftplib
import os
import re
import importlib
from color import *

#--------------------------------------
# Default connection settings
#--------------------------------------
state = "idle"
address = "127.0.0.1"
user = ""
password = ""
port="21"
acct = ""
tmp = ""

class Ftp(ftplib.FTP):
    def __init__(self, address, user, password, acct):
        ftplib.FTP.__init__(self, address, user, password, acct)

    def is_dir(self, name):
        r1 = re.findall(r"type=(file|dir)", self.sendcmd('MLST {}'.format(name)))
        type = ''.join(r1)
        return type == "dir"

    def create_parent_dir(self, fpath):
        dirname = os.path.dirname(fpath)
        while not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
                print("created directory : {0}".format(dirname))
            except:
                create_parent_dir(dirname)

    def download_file(self, name, dest, overwrite):
        self.create_parent_dir(dest.lstrip("/"))
        if not os.path.exists(dest) or overwrite is True:
            try:
                with open(dest, 'wb') as f:
                    self.retrbinary("RETR {0}".format(name), f.write)
                print("Downloaded: {0}".format(dest))
            except FileNotFoundError:
                print("FAILED: {0}".format(dest))
        else:
            print("Already exists: {0}".format(dest))

    def download_tree(self, path, overwrite=False):
        path = path.lstrip("/")
        original_directory = os.getcwd()
        self.mirror_dir(path, overwrite)
        os.chdir(original_directory)

    def mirror_dir(self, name, overwrite):
        for item in self.nlst(name):
            if self.is_dir(item): # if it is a directory then we don't care
                self.mirror_dir(item, overwrite)
            else:
                self.download_file(item, item, overwrite)


#--------------------------------------
# Connector
#--------------------------------------

def connect(address="127.0.0.1", user="", password="", port="21", acct=""):
        try:
            ftp = Ftp(address, user, password, acct)
            # ftp.connect(address, int(port))
            return ("connected", ftp)
        except ftplib.all_errors as e:
            return ("failed", e)

while state != "connected":
    if state == "failed":
        error("FTP failed to connect: {}".format(res))

    tmp = input("FTP Host ({}): ".format(address))
    address = tmp if tmp != "" else address

    tmp = input("FTP User ({}): ".format(user))
    user = tmp if tmp != "" else user

    tmp = input("FTP Password: ")
    password = tmp if tmp != "" else password

    tmp = input("FTP Port ({}): ".format(port))
    port = tmp if tmp != "" else port

    tmp = input("FTP Account Name ({}): ".format(acct))
    acct = tmp if tmp != "" else acct

    state, ftp = connect(address, user, password, port, acct)

# print welcome message
success("You are now connected to server")
color("\n[b]Welcome {}![/b] I am:\n{}\n".format(user, ftp.getwelcome()), True)

#--------------------------------------
# Interpreter
# --------------------------------------

exit = False
while exit == False:
    commands = input(color("[b][green]ftp://{}@{}:[blue]{}[/endc][b]$>[/endc] ".format(user, address, ftp.pwd())))
    if commands == "":
        continue
    commands = commands.split(" & ")

    for command in commands:
        command = command.split()
        if len(command) == 0:
            print("Syntax Error: Part of given command line is invalid")
            break
        try:
            cmd = importlib.import_module("commands.{}".format(command[0]))
            cls = getattr(cmd, command[0])
            cls = cls(command, ftp, address, user)
            cls.call()
            ftp = cls.ftp
        except:
            print('command {} not found. Type help to see available commands'. format(command[0]))
            break
        if command[0] == "exit":
            exit = True
            break
