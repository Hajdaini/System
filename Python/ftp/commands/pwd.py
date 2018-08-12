#coding:utf-8

from modules.Command import Command

class pwd(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        print(self.ftp.pwd())
