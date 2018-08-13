# coding:utf-8

from modules.Command import Command
from modules.color import error, warning
from modules.Capture import Capture


class cat(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)
        self.error_message = "Usage : cat [OPTION] <filename>"

    def call(self):
        self.input_error_handle(self.without_options_handle, self.with_options_handle, 'file')

    def without_options_handle(self):
        path = self.ftp.sabspath(self.argv[1])
        self.ftp.retrlines("RETR " + path, print(end=""))

    def with_options_handle(self):
        path = self.ftp.sabspath(self.argv[2])
        opts = self.argv[1]
        self.options_handle(path, opts)

    def options_handle(self, path, opts=""):
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
            elif "n" in opts:
                el = "\t{} {}".format(idx + 1, el)
            if "b" in opts and el != "" and el != "$":
                counter += 1
            if not "s" in opts or ("s" in opts and el != "" and el != "$"):
                print(el)