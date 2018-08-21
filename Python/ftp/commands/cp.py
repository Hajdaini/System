# coding:utf-8

from modules.Command import Command
from modules.color import warning

class cp(Command):
    """
    [b]SYNOPSIS[/b]

        [b]cp[/b]   [[b]SOURCE[/b]] [[u]DESTINATION[/u]]

    [b]DESCRIPTION[/b]

         copy files and directories within server. if DESTINATION path is not set, current path will be used
    """

    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        self.input_handle()

    def used_without_options(self):
        if self.argc == 2:
            self.argv.append("./")
        self.ftp.cp(self.argv[1], self.argv[2])

    def handle_error(self):
        warning("Command takes at least a source file")
        self.help()
