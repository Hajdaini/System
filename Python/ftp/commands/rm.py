# coding:utf-8

import time

from modules.Command import Command
from modules.color import cprint
from modules.color import warning
from modules.Benchmark import Benchmark as Bench

class rm(Command):
    """
    [b]SYNOPSIS[/b]

        [b]rm[/b]   [[u]OPTION[/u]] [u]PATH[/u]

    [b]DESCRIPTION[/b]

        remove files or directories

    [b]OPTIONS[/b]

        [b]-d[/b]
            remove a directory if it is empty

        [b]-r[/b]
            remove a directory and all its contents
    """

    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        Bench.mark("start")
        self.input_handle()
        Bench.elapsed_time("start")

    def used_without_options(selff):
        abs_path = self.ftp.sabspath(self.argv[1])
        if self.ftp.is_file(abs_path):
            self.del_file(abs_path)
        else:
            warning("{} is not a filename (for directory use \" rm -d <directory>\")".format(abs_path))

    def used_with_options(self):
        path = self.ftp.sabspath(self.argv[2])
        self.options_handle()

    def options_handle(self):
        options = self.argv[1]
        if "R" in options or "r" in options:
            for idx, el in enumerate(self.argv):
                if idx >= 2:
                    if self.ftp.is_dir(el) and self.ftp.is_empty(el):
                        self.del_dir(el)
                    else:
                        warning(el + " is not a directory or not empty")
        elif "D" in options or "d" in options:
            for idx, el in enumerate(self.argv):
                if idx >= 2:
                    self.del_recursive(self.ftp.sabspath(el))
        else:
            warning('invalid options')

    def del_recursive(self, path):
        if self.ftp.is_file(path):
            self.del_file(path)
        else:
            cnt = self.ftp.ls_info(path)
            if len(cnt):
                for key, el in cnt.items():
                    if el["type"] == "file":
                        srcpath = self.ftp.abspath(path, el["name"])
                        self.del_file(srcpath)
                        cprint("{}...[green]OK[/green]".format(srcpath))
                    else:
                        self.del_recursive(self.ftp.abspath(path, el["name"]))
            self.del_dir(path)

    def del_file(self, path):
        path = self.ftp.sabspath(path)
        self.ftp.delete(path)

    def del_dir(self, path):
        path = self.ftp.sabspath(path)
        self.ftp.rmd(path)
        cprint("{}...[green]OK[/green]".format(path))

    def handle_error(self):
        warning("Command takes at least one file path")
        self.help()
