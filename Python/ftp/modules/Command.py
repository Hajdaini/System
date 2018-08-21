# coding:utf-8
from modules.color import error, warning, fatal, cprint
from modules.Loader import Loader

class Command:
    def __init__(self, args, ftp):
        self.argc = len(args)
        self.argv = args
        self.ftp = ftp
        self.address = self.ftp.address
        self.user = self.ftp.user
        self.util = Loader().load("utils")

    def help(self):
        if self.__doc__ != None:
            cprint(self.__doc__)
        else:
            warning("Unavailable documentation")

    def input_handle(self):
        nargs = self.argc - 1
        hasoption = nargs >= 1 and self.argv[1][0] == "-"
        nfiles = nargs - 1 if hasoption else nargs
        if not nargs:
            self.used_alone()
        elif nargs == 1:
            if not hasoption:
                self.used_without_options()
            elif hasoption:
                self.used_alone_with_options()
        elif nargs >= 2:
            if hasoption:
                self.used_with_options()
            elif not hasoption:
                self.used_without_options()

    def used_alone(self): # ls
        self.handle_error()

    def used_alone_with_options(self): # ls -l
        self.handle_error()

    def used_without_options(self): # ls path
        self.handle_error()

    def used_with_options(self): # ls -l path
        self.handle_error()

    def handle_error(self):
        pass
