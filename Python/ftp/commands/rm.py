#coding:utf-8

from modules.Command import Command
from modules.color import error, cprint
from modules.color import warning
import time

class rm(Command):
    """
    [b]SYNOPSIS[/b]

        [b]rm[/b]   [[u]OPTION[/u]]...[u]PATH[/u]

    [b]DESCRIPTION[/b]

        remove files or directories

    [b]OPTIONS[/b]

        [b]-d[/b]
            remove directory recursively

        [b]-r[/b]
            Anthraxx put something here

    """

    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def without_options_handle(self):
        abs_path = self.ftp.sabspath(self.argv[1])
        if self.ftp.is_file(abs_path):
            self.del_file(abs_path)
        else:
            warning("{} is not a filename (for directory use \" rm -d <directory>\")".format(abs_path))

    def with_options_handle(self):
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

    def call(self):
        start_time = time.time()
        self.input_error_handle(self.without_options_handle, self.with_options_handle)
        info("Elapsed time: {0:.4f}s".format(time.time() - start_time))

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
