#coding:utf-8

from commands.Command import Command

from color import warning

class ls(Command):
    def __init__(self, args, ftp, address, user):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        if self.argc == 1:
            self.ftp.dir()
        elif self.argc == 2:
            self.ftp.dir(self.argv[1])
        else:
            warning("(Usage : ls <path>)")
