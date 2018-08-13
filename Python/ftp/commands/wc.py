# coding:utf-8

import re
from modules.Command import Command
from modules.color import error, warning
from modules.Capture import Capture


class wc(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        self.input_error_handle(self.without_options_handle, self.with_options_handle, 'file')

    def without_options_handle(self):
        path = self.ftp.sabspath(self.argv[1])
        self.output_handle(path)

    def with_options_handle(self):
        path = self.ftp.sabspath(self.argv[2])
        self.output_handle(path, self.argv[1])

    def output_handle(self, path, options="all"):
        output = ""
        with Capture() as stdout:
            self.ftp.retrlines("RETR " + path, print(end=""))
        res = " ".join(stdout)
        if "l" in options or "L" in options or options == "all":
            output = "{}lines: {}\n".format(output, len(stdout))
        if "w" in options or "W" in options or options == "all":
            count = len(re.findall(r'\w+', res))
            output = "{}words: {}\n".format(output, count)
        if "c" in options or "C" in options or options == "all":
            output = "{}characters: {}".format(output, len(res))
        print("{} :\n{}".format(path, output))