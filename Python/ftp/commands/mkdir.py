#coding:utf-8

from commands.Command import Command
from modules.color import error

class mkdir(Command):
    def __init__(self, args, ftp, address, user):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        try:
            file = "{}/{}".format(self.ftp.pwd(), self.argv[1])
            self.ftp.mkd(file)
        except :
            error("You may not have permission to create folder")
