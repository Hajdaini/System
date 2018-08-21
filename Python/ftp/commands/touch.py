# coding:utf-8
import io

from modules.Command import Command
from modules.color import warning

class touch(Command):
    """
    [b]SYNOPSIS[/b]

        [b]touch[/b]   [u]FILE[/u]

    [b]DESCRIPTION[/b]

        create a new blank file on server
    """

    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        self.input_handle()

    def used_without_options(self):
        for file in self.argv[1:]:
            try:
                self.ftp.storbinary('STOR {}'.format(file), io.BytesIO(b''))
            except:
                warning("Could nor create file: " + file)

    def handle_error(self):
        warning("Command takes at least one file path")
        self.help()
