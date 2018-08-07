#coding:utf-8

from commands.Command import Command

class exit(Command):
    def __init__(self, args, ftp, address, user):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        print("Good Bye {}!".format(self.user if self.user != "" else "Anonymous"))
