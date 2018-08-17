# coding:utf-8

import re
from modules.Command import Command
from modules.color import *
import time


class df(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)
        self.total_size = []

    def used_alone(self):
        self.output_handle('.')

    def used_alone_with_options(self):
        if "h" in self.argv[1] or "H" in self.argv[1]:
            self.output_handle('.', True)
        else:
            warning("invalid options")

    def used_without_options(self):
        self.output_handle(self.argv[1])

    def used_with_options(self):
        if "h" in self.argv[1] or "H" in self.argv[1]:
            self.output_handle(self.argv[2], True)
        else:
            warning("invalid options")

    def call(self):
        start_time = time.time()
        self.input_error_handle(self.used_without_options, self.used_with_options, 'both', True, True, self.used_alone,
                                self.used_alone_with_options)
        info("Finish in {0:.4f} s\n".format(time.time() - start_time))

    def output_handle(self, path_to_verify, human_size=False):
        path_to_verify = self.ftp.sabspath(path_to_verify)
        for path in self.ftp.nlst(path_to_verify):
            if self.ftp.is_dir(path):
                self.print_directory_size(path, human_size)
                self.print_total_size(human_size)
            else:
                if human_size is True:
                    cprint("[warning]{}[/warning] : {}".format(self.byte_convert(self.ftp.size(path)), path))
                else:
                    size = self.ftp.size(path)
                    self.total_size.append(size)
                    print("[warning]{}[/warning] : {}".format(size, path))

    def print_total_size(self, human_size):
        total = sum(self.total_size)
        if human_size is True:
            cprint("[green]Total : {}[/green]\n".format(self.byte_convert(total)))
        else:
            cprint("[green]Total : {}[/green]\n".format(total))
        self.total_size = []

    def print_directory_size(self, directory, human_size=False):
        for path in self.ftp.nlst(directory):
            try:
                abs_path = self.ftp.sabspath(path)
                if self.ftp.is_dir(abs_path):
                    self.print_directory_size(abs_path, human_size)
                else:
                    size = self.ftp.size(abs_path)
                    self.total_size.append(size)
                    if human_size:
                        print("[warning]{}[/warning] : {}".format(self.byte_convert(size), path))
                    else:
                        print("[warning]{}[/warning] : {}".format(size, path))
            except:
                warning("You dont have permission for: {}".format(abs_path))

    def byte_convert(self, n):
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.1f%s' % (value, s)
        return "%sB" % n
