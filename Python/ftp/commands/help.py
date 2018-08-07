#coding:utf-8

from commands.Command import Command

class help(Command):
    def __init__(self, args, ftp, address, user):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        pass
