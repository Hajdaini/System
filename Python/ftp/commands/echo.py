# coding:utf-8

from modules.Command import Command


class echo(Command):
    """
    [b]SYNOPSIS[/b]

        [b]echo[/b]   [u]STRING[/u]

    [b]DESCRIPTION[/b]

        display a line of text
    """
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        del self.argv[0]
        print(" ".join(self.argv))
