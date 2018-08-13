# coding:utf-8

from modules.Command import Command
from modules.color import error


class put(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        self.ftp.push(self.argv[1])
