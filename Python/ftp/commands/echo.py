# coding:utf-8

from modules.Command import Command
from modules.color import warning

class echo(Command):
    """
    [b]SYNOPSIS[/b]

        [b]echo[/b]   [[b]STRING[/b]]

    [b]DESCRIPTION[/b]

        display a STRING on standard output
    """

    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        if self.argc >= 2:
            del self.argv[0]
            print(" ".join(self.argv))
        else:
            warning("Require content to display")
            self.help()
