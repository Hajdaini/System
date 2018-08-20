# coding:utf-8

from modules.Command import Command


class welcome(Command):
    """
    [b]SYNOPSIS[/b]

        [b]welcome[/b]

    [b]DESCRIPTION[/b]

        print the welcome message of the remote machine
    """
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        print(self.ftp.getwelcome())
