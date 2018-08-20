# coding:utf-8
import os

from modules.Command import Command


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
        os.system('cls' if os.name == 'nt' else 'clear')
