# coding:utf-8

import re
from modules.Capture import Capture
from modules.Command import Command
from modules.color import warning

class cat(Command):
    """
    [b]SYNOPSIS[/b]

        [b]cat[/b]   [[u]OPTIONS[/u]] [u]FILE[/u]...

    [b]DESCRIPTION[/b]

        print file on standard output

    [b]OPTIONS[/b]

        [b]-A[/b]
            equivalent to [b]-vET[/b]

        [b]-b[/b]
             number nonempty output lines, overrides [b]-n[/b]

        [b]-e[/b]
            equivalent to [b]-vE[/b]

        [b]-E[/b]
             Display an [b]$[/b] at end of each line

        [b]-n[/b]
            number all output lines, including empty ones

        [b]-s[/b]
            suppress repeated empty lines

        [b]-t[/b]
            equivalent to [b]-vT[/b]

        [b]-T[/b]
            Display TAB character as [b]^I[/b]

        [b]-v[/b]
            Display all non printable characters as [b]^M[/b] excepted \t and \n
    """

    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)
        self.error_message = "Usage : cat [OPTION] <filename>"

    def call(self):
        if self.argc == 2 and " " in self.argv[1]:
            self.argv = self.argv[1].split()
        self.input_handle()

    def used_without_options(self):
        for file in self.argv[1:]:
            path = self.ftp.sabspath(file)
            try:
                self.ftp.retrlines("RETR " + path, print(end=""))
            except:
                warning("Invalid file: " + file)

    def used_with_options(self):
        opts = self.argv[1]
        for file in self.argv[2:]:
            path = self.ftp.sabspath(file)
            self.options_handle(path, opts)

    def options_handle(self, path, opts=""):
        try:
            counter = 1
            with Capture() as stdout:
                self.ftp.retrlines("RETR " + path, print(end=""))
            for idx, el in enumerate(stdout):
                if "E" in opts or "A" in opts or "e" in opts:
                    el += "$"
                if "T" in opts or "t" in opts:
                    el = el.replace("\t", "^I")
                if "b" in opts and el != "" and el != "$":
                    el = "\t{} {}".format(counter, el)
                if "v" in opts or "A" in opts or "e" in opts or "t" in opts:
                    el = re.sub(r'[^\x00-\x7F]+', '^M', el)
                if "b" in opts and el != "" and el != "$":
                    counter += 1
                elif "n" in opts:
                    el = "\t{} {}".format(idx + 1, el)
                if not "s" in opts or ("s" in opts and el != "" and el != "$"):
                    print(el)
        except:
            warning("Invalid file: " + path.split("/")[-1])

    def handle_error(self):
        warning("Filename missing")
