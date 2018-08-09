#coding:utf-8

from commands.Command import Command

from modules.color import warning, color
from modules.Capture import Capture

class ls(Command):
    """
    NAME: ls

    Lists the folder's content

    SYNOPSIS:

    ls

    DESCRIPTION:

    Called with no arguments. It is designed to display a folder's content like a regular ls -l call.
    """
    def __init__(self, args, ftp, address, user):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        if self.argc == 1:
            with Capture() as output:
                self.ftp.dir()
            self.colorize(output)
        elif self.argc == 2:
            with Capture() as output:
                file = self.ftp.abspath(self.argv[1])
                self.ftp.dir(file)
            self.colorize(output)
        else:
            warning("(Usage : ls <path>)")

    def colorize(self, list):
        for el in list:
            spl = el.split()
            if spl[0][0] == "d":
                spl[len(spl) - 1] = "[b][blue]{}[/endc]".format(spl[len(spl) - 1])
            color(" ".join(spl), True)
