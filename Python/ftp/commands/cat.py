# coding:utf-8

from modules.Command import Command
from modules.color import error, warning
from modules.Capture import Capture


class cat(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)
        self.error_message = "Usage : cat [OPTION] <filename>"

    def call(self):
        if self.input_error_handle(self.methode1, self.methode2):
            return

        """if self.ftp.is_file(self.argv[1]):
            path = self.ftp.sabspath(self.argv[1])
            self.ftp.retrlines("RETR " + path, print(end=""))
        elif self.argv[1][0] == "-" and self.argc == 3:
            path = self.ftp.sabspath(self.argv[2])
            opts = self.argv[1]
            self.cat_file(path, opts)"""

    def methode1(self):
        path = self.ftp.sabspath(self.argv[1])
        self.ftp.retrlines("RETR " + path, print(end=""))

    def methode2(self):
        path = self.ftp.sabspath(self.argv[2])
        opts = self.argv[1]
        self.cat_file(path, opts)

    def cat_file(self, path, opts=""):
        counter = 1
        try:
            with Capture() as stdout:
                self.ftp.retrlines("RETR " + path, print(end=""))
        except:
            warning("Invalid file: " + path)
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

"""
#coding:utf-8

from modules.Command import Command
from modules.color import error, warning
from modules.Capture import Capture


class cat(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        if self.argc == 1:
            warning("Filename missing")
            return
        opts = self.argv[1] if self.argv[1][0] == "-" and not self.ftp.is_file(self.argv[1]) else ""
        if opts != "" and self.argc < 3:
            warning("Filename missing")
            return
        for idx, el in enumerate(self.argv):
            if (idx >= 1 and opts == "") or (idx >= 2 and opts != ""):
                self.cat_file(el, opts)

    def cat_file(self, path, opts=""):
        counter = 1
        path = self.ftp.abspath(path)
        try:
            with Capture() as stdout:
                self.ftp.retrlines("RETR " + path, print(end=""))
        except:
            warning("Invalid file: " + path)
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
"""
