#coding:utf-8

from commands.Command import Command
from modules.color import error

class rm(Command):
    def __init__(self, args, ftp, address, user):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        file = "{}/{}".format(self.ftp.pwd(), self.argv[1])
        try:
            folder = "{}/{}".format(self.ftp.pwd(), self.argv[2])
        except:
            pass
        try:
            if self.argv[1] == '-d' or self.argv[1] == '-D':
                self.ftp.rmd(folder)
            else:
                self.ftp.delete(file)
        except:
            error("You may not have permission to delete file or folder (use option -d to delete folder)")
