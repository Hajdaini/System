# coding:utf-8

from modules.Command import Command
from modules.color import warning

class get(Command):
    """
    [b]SYNOPSIS[/b]

        [b]get[/b]   [[b]SOURCE[/b]] [u]DESTINATION[/u]

    [b]DESCRIPTION[/b]

        download file or directory from server to local machine
    """

    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        self.input_handle()

    def used_without_options(self):
        if self.argc == 2:
            self.argv.append("./")
        self.ftp.pull(self.argv[1], self.argv[2])

    def handle_error(self):
        warning("Command takes at least a source path")
        self.help()
