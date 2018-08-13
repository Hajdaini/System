# coding:utf-8

from modules.Command import Command

from modules.color import warning, color, cprint, error
from modules.Capture import Capture


class ls(Command):
    """
    NAME: ls

    Lists the folder's content

    SYNOPSIS:

    ls

    DESCRIPTION:

    Called with no arguments. It is designed to display a folder's content like a regular ls -l call.
    """

    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        if self.argc == 1:
            ls_info_dict = self.ftp.ls_info()
            self.print_ls_wihout_options(ls_info_dict)
        elif self.argc == 2 and not self.argv[1][0] == "-":
            if self.ftp.exists(self.argv[1]):
                ls_info_dict = self.ftp.ls_info(self.argv[1])
                self.print_ls_wihout_options(ls_info_dict)
            else:
                warning("Invalid path: " + self.argv[1])
        elif self.argc == 2 and 'l' in self.argv[1] and self.argv[1][0] == "-":
            self.print_ls_with_options('.')
        elif self.argc == 3 and 'l' in self.argv[1]:
            if self.ftp.exists(self.argv[2]):
                self.print_ls_with_options(self.argv[2])
            else:
                warning("Invalid path: " + self.argv[2])
        else:
            error("(Usage : ls <path>)")

    def print_ls_wihout_options(self, ls_info_dic):
        output = ""
        for filename, info in ls_info_dic.items():
            if info["type"] == "dir":
                output += "[blue]{}[/blue]/    ".format(filename)
            else:
                output += "{}    ".format(filename)
        print(output)

    def print_ls_with_options(self, path):
        with Capture() as output:
            self.ftp.dir(path)
        self.colorize(output)

    def colorize(self, list):
        for el in list:
            spl = el.split()
            if spl[0][0] == "d":
                spl[len(spl) - 1] = "[b][blue]{}[/endc]/".format(spl[len(spl) - 1])
            color(" ".join(spl), True)
