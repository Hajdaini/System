#coding:utf-8
import os

from commands.Command import Command

class clear(Command):
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
       os.system('cls' if os.name=='nt' else 'clear')
