# coding:utf-8

from modules.Command import Command
from modules.color import warning

class mkdir(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        if self.argc >= 2:
            for file in self.argv[1:]:
                try:
                    if not self.ftp.exists(file):
                        file = self.ftp.sabspath(file)
                        self.ftp.mkd(file)
                    else:
                        warning("File or directory already exists: " + file)
                except:
                    error("You may not have permission to create folder: " + file)
        else:
            warning("Filename missing")
