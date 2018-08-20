# coding:utf-8

from modules.Command import Command

class cp(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        self.ftp.cp(self.argv[1], self.argv[2])
