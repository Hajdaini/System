#coding:utf-8

#--------------------------------------
# Imports
#--------------------------------------

import sys
import ftplib
import os
import re
import sys
import importlib
from getpass import getpass
from color import *
from capture import Capture
from Ftp import Ftp

#--------------------------------------
# Default connection settings
#--------------------------------------

state = "idle"
address = "127.0.0.1"
user = ""
password = ""
port=21
timeout=30
tmp = ""

#--------------------------------------
# Connector
#--------------------------------------

def connect(address="127.0.0.1", user="", password="", port="21", timeout=30):
        try:
            ftp = Ftp(address, timeout)
            ftp.connect(address, int(port))
            ftp.login(user, password)
            return ("connected", ftp)
        except ftplib.all_errors as e:
            return ("failed", e)

while state != "connected":
    if state == "failed":
        error("FTP failed to connect: {}".format(ftp))
    try:
        tmp = input("FTP Host ({}): ".format(address))
        address = tmp if tmp != "" else address

        tmp = input("FTP User ({}): ".format(user))
        user = tmp if tmp != "" else user

        tmp = getpass("FTP Password: ")
        password = tmp if tmp != "" else password

        tmp = input("FTP Port ({}): ".format(port))
        port = int(tmp) if tmp != "" else port

        tmp = input("FTP Connection Timeout ({} seconds): ".format(timeout))
        timeout = int(tmp) if tmp != "" else timeout

    except KeyboardInterrupt:
        color("\n[b]Good Bye {}![/b]".format(user), True)
        sys.exit(1)
    state, ftp = connect(address, user, password, port, timeout)

# Preparing server
ftp.encoding = 'utf-8'

# print welcome message
success("You are now connected to server")
cprint("\n[b]Welcome {}![/b] I am:\n{}\n".format(user, ftp.getwelcome()))

#--------------------------------------
# Interpreter
# --------------------------------------

while True:
    try:
        commands = input(color("[b][green]ftp://{}@{}:[blue]{}[/endc][b]$>[/endc] ".format(user, address, ftp.pwd())))
    except KeyboardInterrupt:
        print("\nGood Bye {}!".format(user))
        sys.exit(1)
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
