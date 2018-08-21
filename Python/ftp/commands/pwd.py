# coding:utf-8

from modules.Command import Command

class pwd(Command):
    """
    [b]SYNOPSIS[/b]

        [b]pwd[/b]

    [b]DESCRIPTION[/b]

        print name of current/working directory
    """

    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        self.input_handle()

    def used_alone(self):
        print(self.ftp.pwd())

    def handle_error(self):
        warning("This command takes no arguments")
        self.help()
