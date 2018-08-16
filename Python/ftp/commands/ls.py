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
        path = self.ftp.sabspath(path)
        with Capture() as nlst:
            if "a" in self.argv[1] or "A" in self.argv[1]:
                self.ftp.retrlines("NLST -a " + path)
            else:
                self.ftp.retrlines("NLST " + path)
        if "l" in self.argv[1] or "L" in self.argv[1]:
            with Capture() as output:
                if "a" in self.argv[1] or "A" in self.argv[1]:
                    self.ftp.retrlines("LIST -a {}".format(path))
                else:
                    self.ftp.retrlines("LIST {}".format(path))
            self.colorize(output, nlst)
        elif "a" in self.argv[1] or "A" in self.argv[1]:
            with Capture() as output:
                self.ftp.retrlines("LIST -a {}".format(path))
            for idx, el in enumerate(output):
                file = nlst[idx]
                output[idx] = "[b][blue]{}[/endc]/".format(file.replace("/", "")) if el[0] == "d" else file
            cprint("    ".join(output))
        else:
            warning("invalid options")

    def colorize(self, list, nlst):
        for idx, el in enumerate(list):
            file = nlst[idx].split("/")[-1]
            line = el[0:(len(file) * -1)]
            if file[0] == ".":
                if line[0] == "d":
                    file = "[b][blue]{}[/endc]/".format(file.replace("/", ""))
                else:
                    file = "[b][header]{}[/endc]".format(file.replace("/", ""))
            elif line[0] == "d":
                file = "[b][blue]{}[/endc]/".format(file)
            cprint("{} {}".format(line, file))
