#coding:utf-8

#--------------------------------------
# Imports
#--------------------------------------

import sys
import ftplib
import os
import re
import importlib
from getpass import getpass
from color import *
from capture import Capture

#--------------------------------------
# Ftp class
#--------------------------------------

class Ftp(ftplib.FTP):
    def __init__(self):
        ftplib.FTP.__init__(self)

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
# Default connection settings
#--------------------------------------

state = "idle"
address = "127.0.0.1"
user = ""
password = ""
port="21"
tmp = ""

#--------------------------------------
# Connector
#--------------------------------------

def connect(address="127.0.0.1", user="", password="", port="21"):
        try:
            ftp = Ftp()
            ftp.connect(address, int(port))
            ftp.login(user, password)
            # ftp = Ftp(address, user, password)
            # ftp.connect(address, int(port))
            return ("connected", ftp)
        except ftplib.all_errors as e:
            return ("failed", e)

while state != "connected":
    if state == "failed":
        error("FTP failed to connect: {}".format(ftp))

    tmp = input("FTP Host ({}): ".format(address))
    address = tmp if tmp != "" else address

    tmp = input("FTP User ({}): ".format(user))
    user = tmp if tmp != "" else user

    tmp = getpass("FTP Password: ")
    password = tmp if tmp != "" else password

    tmp = input("FTP Port ({}): ".format(port))
    port = tmp if tmp != "" else port

    state, ftp = connect(address, user, password, port)

# Preparing server
ftp.encoding = 'utf-8'

# print welcome message
success("You are now connected to server")
color("\n[b]Welcome {}![/b] I am:\n{}\n".format(user, ftp.getwelcome()), True)

#--------------------------------------
# Interpreter
# --------------------------------------

while True:
    commands = input(color("[b][green]ftp://{}@{}:[blue]{}[/endc][b]$>[/endc] ".format(user, address, ftp.pwd())))
    if commands == "":
        continue
    commands = commands.split(" & ")
    for pipes in commands:
        stdin = None
        if len(pipes) == 0:
            print("Syntax Error: Part of given command line is invalid")
            break
        pipes = pipes.split(" | ")
        for idx, pipe in enumerate(pipes):
            if len(pipe) == 0:
                print("Syntax Error: Part of given command line is invalid")
                break
            pipe = pipe.split()
            if stdin != None and len(stdin):
                command = [pipe[0], stdin]
            else:
                command = pipe
            """
            print("{} {}".format(pipe, command))
            cmd = importlib.import_module("commands.{}".format(command[0]))
            cls = getattr(cmd, command[0])
            cls = cls(command, ftp, address, user)
            with Capture() as stdin:
                cls.call()
            if idx == len(pipes) - 1 and stdin != None and len(stdin):
                for str in stdin:
                    print(str)
            ftp = cls.ftp
            """
            try:
                cmd = importlib.import_module("commands.{}".format(command[0]))
                cls = getattr(cmd, command[0])
                cls = cls(command, ftp, address, user)
                with Capture() as stdin:
                    cls.call()
                if idx == len(pipes) - 1 and stdin != None and len(stdin):
                    for str in stdin:
                        print(str)
                elif idx < len(pipes) - 1 and stdin != None and len(stdin):
                    stdin = "\n".join(stdin)
                ftp = cls.ftp
            except:
                warning('command {} not found. Type help to see available commands'. format(command[0]))
                break
            if command[0] == "exit":
                sys.exit(1)
