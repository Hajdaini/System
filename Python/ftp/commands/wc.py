# coding:utf-8

import re
from modules.Command import Command
from modules.color import error, warning
from modules.Capture import Capture


class wc(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        slen = len(self.argv[1])
        if slen > 1:
            opts = self.argv[1]
            type = opts[1:] if opts[0] == "-" and not self.ftp.is_file(opts) else None
            for idx, el in enumerate(self.argv):
                if (type == None and idx) or (type != None and idx >= 2):
                    self.wc(el, type)
        else:
            warning("No file specified")

    def wc(self, path, type=None):
        output = " "
        path = self.ftp.abspath(path)
        try:
            with Capture() as stdout:
                self.ftp.retrlines("RETR " + path, print(end=""))
        except:
            warning("Invalid file given: " + path)
            return
        res = " ".join(stdout)
        if type == None or "l" in type:
            output = "{} lines:{}".format(output, len(stdout))
        if type == None or "w" in type:
            count = len(re.findall(r'\w+', res))
            if type == None or len(type):
                output = "{} words:{}".format(output, count)
            else:
                output = "{}words:{}".format(output, count)
        if type == None or "c" in type:
            if type == None or len(type):
                output = "{} characters:{}".format(output, len(res))
            else:
                output = "{}characters:{}".format(output, len(res))
        file = path.split("/")
        print("{} {}".format(output, file[-1]))
