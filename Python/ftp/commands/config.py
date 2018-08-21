# coding:utf-8

from modules.Command import Command
from modules.Config import Config
from modules.color import *

class config(Command):
    """
    [b]SYNOPSIS[/b]

        [b]config[/b]

    [b]DESCRIPTION[/b]

         display config of your ftp client
    """

    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        self.input_handle()

    def used_alone(self):
        Config.display_config()

    def handle_error(self):
        warning("This command takes no argument")
        self.help()
