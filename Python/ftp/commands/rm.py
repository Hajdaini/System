#coding:utf-8

from modules.Command import Command
from modules.color import error
from modules.path import abspath
from modules.color import warning

class rm(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        if len(self.argv) >= 3 and (self.argv[1] == "-d" or self.argv[1] == "-D"):
            for idx, el in enumerate(self.argv):
                if idx >= 2:
                    if self.ftp.is_dir(el) and self.ftp.is_empty(el):
                        self.del_dir(el)
                    else:
                        warning(el + " is not a directory or not empty")
        elif len(self.argv) >= 3 and (self.argv[1] == "-r" or self.argv[1] == "-R"):
            for idx, el in enumerate(self.argv):
                if idx >= 2:
                    self.del_recursive(self.ftp.abspath(el))
        else:
            for idx, el in enumerate(self.argv):
                if idx >= 1:
                    el = self.ftp.abspath(el)
                    if self.ftp.is_file(el):
                        self.del_file(el)
                    else:
                        warning(el + " is not a file or permission denied")

    def del_recursive(self, path):
        if self.ftp.is_file(path):
            self.del_file(path)
        else:
            cnt = self.ftp.ls_info(path)
            if len(cnt):
                for key, el in cnt.items():
                    if el["type"] == "file":
                        self.del_file(abspath(path, el["name"]))
                    else:
                        self.del_recursive(abspath(path, el["name"]))
            self.del_dir(path)

    def del_file(self, path):
        path = self.ftp.abspath(path)
        self.ftp.delete(path)

    def del_dir(self, path):
        path = self.ftp.abspath(path)
        self.ftp.rmd(path)
