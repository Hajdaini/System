# coding:utf-8
import os

from modules.Command import Command
from modules.color import warning

class clear(Command):
    """
    [b]SYNOPSIS[/b]

        [b]clear[/b]

    [b]DESCRIPTION[/b]

         clear the terminal screen
    """

    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        self.input_handle()

    def used_alone(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def handle_error(self):
        warning("This command takes no arguments")
        self.help()
