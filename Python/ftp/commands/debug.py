#coding:utf-8

from modules.Command import Command
from modules.color import warning, info

class debug(Command):
    def __init__(self,rgs, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        if self.argc == 2:
            debugging = int(self.argv[1])
            if debugging == 0 or debugging == 1:
                self.ftp.debugging = debugging
                info("Debug mode: {} ({})".format("enabled" if self.ftp.debugging else "disabled", self.ftp.debugging))
            else:
                warning("Debug mode must be 0 or 1")
        elif self.argc == 1:
            info("Debug mode: {} ({})".format("enabled" if self.ftp.debugging else "disabled", self.ftp.debugging))
        else:
            warning("Usage: debug <mode>")
