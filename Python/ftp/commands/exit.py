#coding:utf-8

from modules.Command import Command
from modules.color import color

class exit(Command):
    def __init__(self, args, ftp, address, user):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        color("[b]Good Bye {}![/b]".format(self.user if self.user != "" else "Anonymous"), True)
