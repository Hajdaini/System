#coding:utf-8

from commands.Command import Command

from color import warning, color
from capture import Capture

class ls(Command):
    def __init__(self, args, ftp, address, user):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        if self.argc == 1:
            with Capture() as output:
                self.ftp.dir()
            self.colorize(output)
        elif self.argc == 2:
            with Capture() as output:
                self.ftp.dir(self.argv[1])
            self.colorize(output)
        else:
            warning("(Usage : ls <path>)")

    def colorize(self, list):
        for el in list:
            spl = el.split()
            if spl[0][0] == "d":
                spl[len(spl) - 1] = "[b][blue]{}[/endc]".format(spl[len(spl) - 1])
            color(" ".join(spl), True)
