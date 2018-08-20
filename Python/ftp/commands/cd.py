# coding:utf-8

from modules.Command import Command
from modules.color import error


class cd(Command):
    """
    [b]SYNOPSIS[/b]

        [b]cd[/b]   [u]DIR[/u]

    [b]DESCRIPTION[/b]

        Change the ftp working directory
    """

    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        try:
            if len(self.argv) > 1:
                self.ftp.sendcmd('CWD {}'.format(self.argv[1]))
            else:
                self.ftp.cwd(self.ftp.home)
        except:
            error('Directory may not exist or you may not have permission to view it.')
