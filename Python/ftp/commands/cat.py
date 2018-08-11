	#coding:utf-8

from commands.Command import Command
<<<<<<< HEAD
from modules.color import error, warning
from modules.Capture import Capture
=======
from modules.color import error
>>>>>>> 8edbd2129a35cb6f2c7f103807b961697bfb3c24

class cat(Command):
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        Command.__init__(self, args, ftp, address, user)

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
<<<<<<< HEAD
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
=======
            path = self.ftp.abspath(self.argv[1])
            self.ftp.retrlines("RETR " + path, print(end=""))
        except:
            error('Access denied.')
>>>>>>> 8edbd2129a35cb6f2c7f103807b961697bfb3c24
