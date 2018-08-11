#coding:utf-8

from modules.Command import Command

class pwd(Command):
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        print(self.ftp.pwd())
