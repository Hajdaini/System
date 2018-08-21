# coding:utf-8

from modules.Command import Command
from modules.color import warning


class mkdir(Command):
    """
    [b]SYNOPSIS[/b]

        [b]mkdir[/b]   [u]DIRECTORY[/u]

    [b]DESCRIPTION[/b]

        Create directories if they don't exist
    """

    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        self.input_handle()

    def used_without_options(self):
        for file in self.argv[1:]:
            try:
                if not self.ftp.exists(file):
                    file = self.ftp.sabspath(file)
                    self.ftp.mkd(file)
                else:
                    warning("File or directory already exists: " + file)
            except:
                error("You may not have permission to create folder: " + file)

    def handle_error(self):
        warning("Filename missing")
