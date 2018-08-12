#coding:utf-8

from modules.Command import Command

class welcome(Command):
    def __init__(self,rgs, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        print(self.ftp.getwelcome())
