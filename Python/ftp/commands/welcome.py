#coding:utf-8

from commands.Command import Command

class welcome(Command):
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        print(self.ftp.getwelcome())
