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
        self.input_handle()

    def used_alone(self):
        print(self.ftp.getwelcome())

    def handle_error(self):
        warning("This command takes no arguments")
        self.help()
