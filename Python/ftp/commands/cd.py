# coding:utf-8

from modules.Command import Command
from modules.color import warning


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
        self.input_handle()

    def used_alone(self):
        self.ftp.cwd(self.ftp.home)

    def used_without_options(self):
        try:
            path = self.ftp.sabspath(self.argv[1])
            self.ftp.cwd(path)
        except:
            warning('Directory may not exist or you may not have permission to view it.')

    def handle_error(self):
        warning("This command takes only a path")
        self.help()
