# coding:utf-8

from modules.Command import Command
from modules.color import warning, info


class debug(Command):
    """
    [b]SYNOPSIS[/b]

        [b]debug[/b]   [[u]MODE[/u]]

    [b]DESCRIPTION[/b]

        Set ftp debug mode to get more information about operations

    [b]MODES[/b]

        [b]0[/b]
            Disable all debug information

        [b]1[/b]
            Display general debugging information

        [b]2[/b]
            Add complementary information
    """

    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        if self.argc == 2:
            debugging = int(self.argv[1])
            if debugging >= 0 and debugging <= 2:
                self.ftp.debugging = debugging
                info("Debug mode: {} ({})".format("enabled" if self.ftp.debugging else "disabled", self.ftp.debugging))
            else:
                warning("Debug mode must be 0 or 1")
        elif self.argc == 1:
            info("Debug mode: {} ".format(self.ftp.debugging))
        else:
            warning("Usage: debug [MODE]")
