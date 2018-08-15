# coding:utf-8

from modules.Command import Command
from modules.color import color


class exit(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        color("[b]Good Bye {}![/b]".format(self.ftp.user if self.ftp.user != "" else "Anonymous"), True)
