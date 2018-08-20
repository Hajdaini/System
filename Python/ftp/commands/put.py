# coding:utf-8

from modules.Command import Command

class put(Command):
    """
    [b]SYNOPSIS[/b]

        [b]put[/b]   [u]SOURCE[/u]...[u]DESTINATION[/u]

    [b]DESCRIPTION[/b]

        upload file or directory from the local machine to your remote machine
    """
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        self.ftp.push(self.argv[1])
