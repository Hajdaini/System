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
        self.input_handle()

    def used_without_options(self):
        if self.argc == 2:
            self.argv.append("./")
        self.ftp.push(self.argv[1], self.argv[2])

    def handle_error(self):
        warning("Command takes at least a source path")
        self.help()
