# coding:utf-8

from modules.Command import Command


class echo(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        del self.argv[0]
        print(" ".join(self.argv))
