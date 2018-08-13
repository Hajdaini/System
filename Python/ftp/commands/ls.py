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
        self.input_error_handle(self.used_without_options, self.used_with_options, 'both', True, True, self.used_alone,
                                self.used_alone_with_options)

    def used_alone(self):
        ls_info_dict = self.ftp.ls_info()
        self.print_ls_wihout_options(ls_info_dict)

    def used_without_options(self):
        ls_info_dict = self.ftp.ls_info(self.argv[1])
        self.print_ls_wihout_options(ls_info_dict)

    def used_alone_with_options(self):
        self.print_ls_with_options('.')

    def used_with_options(self):
        self.print_ls_with_options(self.argv[2])

    def print_ls_wihout_options(self, ls_info_dic):
        output = ""
        for filename, info in ls_info_dic.items():
            if info["type"] == "dir":
                output += "[blue]{}[/blue]/    ".format(filename)
            else:
                output += "{}    ".format(filename)
        print(output)

    def print_ls_with_options(self, path):
        if "l" in self.argv[1] or "L" in self.argv[1]:
            with Capture() as output:
                self.ftp.dir(path)
            self.colorize(output)
        else:
            warning("invalid options")

    def colorize(self, list):
        for el in list:
            spl = el.split()
            if spl[0][0] == "d":
                spl[len(spl) - 1] = "[b][blue]{}[/endc]/".format(spl[len(spl) - 1])
            color(" ".join(spl), True)
