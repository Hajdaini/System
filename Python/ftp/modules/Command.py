# coding:utf-8
from modules.color import error, warning


class Command:
    def __init__(self, args, ftp):
        self.argc = len(args)
        self.argv = args
        self.ftp = ftp
        self.address = self.ftp.address
        self.user = self.ftp.user
        self.util = []

    def input_error_handle(self, methode1, methode2):
        if self.argc == 1:
            warning("Filename missing")
            return True
        elif self.argc == 2:
            if not self.ftp.is_file(self.argv[1]):
                warning("Invalid file: " + self.ftp.sabspath(self.argv[1]))
                return True
            else:
                methode1()
                return False
        elif self.argc == 3:
            if not self.ftp.is_file(self.argv[2]):
                warning("Invalid file: " + self.ftp.sabspath(self.argv[2]))
                return True
            elif self.argv[1][0] == "-":
                methode2()
                return False
            else:
                error("usage : {} [OPTION] <path>".format(self.argv[0]))
                return True
        elif self.argc > 3:
            error("usage : {} [OPTION] <path>".format(self.argv[0]))
            return True
        else:
            return False
