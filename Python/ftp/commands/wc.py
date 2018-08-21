# coding:utf-8

import re
from modules.Command import Command
from modules.color import error, warning
from modules.Capture import Capture


class wc(Command):
    """
    [b]SYNOPSIS[/b]

        [b]ls[/b]   [[u]OPTION[/u]]...[u]FILE[/u]

    [b]DESCRIPTION[/b]

        print numbers of line, word and character

    [b]OPTIONS[/b]

        [b]-l[/b]
            print numbers of line

        [b]-w[/b]
            print numbers of word

        [b]-c[/b]
            print numbers of character
    """

    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        self.input_handle()

    def used_without_options(self):
        path = self.ftp.sabspath(self.argv[1])
        self.output_handle(path)

    def used_with_options(self):
        path = self.ftp.sabspath(self.argv[2])
        self.output_handle(path, self.argv[1])

    def output_handle(self, path, options="all"):
        try:
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
        except:
            error("Invalid file type")

    def handle_error(self):
        warning("Command takes at least one file path")
        self.help()
