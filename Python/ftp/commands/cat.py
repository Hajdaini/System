#coding:utf-8

from commands.Command import Command
from modules.color import error

class cat(Command):
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        try:
            path = self.ftp.abspath(self.argv[1])
            self.ftp.retrlines("RETR " + path, print(end=""))
        except:
            error('Access denied.')