# coding:utf-8

from modules.Command import Command
from modules.Config import Config

class config(Command):
    """
    [b]SYNOPSIS[/b]

        [b]config[/b]

    [b]DESCRIPTION[/b]

         show the config of your ftp client
    """

    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        Config.display_config()
