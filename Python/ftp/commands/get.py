# coding:utf-8

from modules.Command import Command

class get(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        self.ftp.pull(self.argv[1], self.argv[2])
