# coding:utf-8

from modules.Command import Command


class get(Command):
    """
    [b]SYNOPSIS[/b]

        [b]get[/b]   [u]SOURCE[/u]...[u]DESTINATION[/u]

    [b]DESCRIPTION[/b]

        download file or directory from the remote machine to your local machine
    """

    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        self.ftp.pull(self.argv[1], self.argv[2])
