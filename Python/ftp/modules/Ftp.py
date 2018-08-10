#coding:utf-8

import io
import os
import re
import os
from modules.color import *
from ftplib import FTP
from modules.path import sabspath, abspath
from modules.Capture import Capture

class Ftp(FTP):
    def __init__(self, host="127.0.0.1", timeout=30):
        FTP.__init__(self, host, timeout=timeout)

    def is_empty(path):
        path = self.abspath(path)
        if not self.exists(path) or self.is_file(path):
            return False
        with Capture() as output:
            self.dir(path)
        return len(output) == 0

    def is_dir(path="./"):
        path = self.abspath(path)
        if len(path) == 1 and path[0] == "/":
            return True
        test = path.split("/")
        test = test[len(test) - 1]
        path = abspath(path, "../")
        ls = self.ls_info(path)
        return test in ls and ls[test]["type"] == "dir"

    def is_file(path):
        path = self.abspath(path)
        if len(path) == 1 and path[0] == "/":
            return False
        test = path.split("/")
        test = test[len(test) - 1]
        path = abspath(path, "../")
        ls = self.ls_info(path)
        return test in ls and ls[test]["type"] == "file"

    def exists(path):
        path = self.abspath(path)
        if len(path) == 1 and path[0] == "/":
            return False
        test = path.split("/")
        test = test[len(test) - 1]
        path = abspath(path, "../")
        ls = self.ls_info(path)
        return test in ls

    def create_parent_dir(self, fpath):
        dirname = os.path.dirname(fpath)
        while not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
                cprint("[warning]the directory {0} has been created successfully[/warning]".format(dirname))
            except:
                cprint("[fail]Failed to create the directory {0}[/fail]".format(dirname))

    def download_file(self, name, dest, overwrite):
        self.create_parent_dir(dest.lstrip("/"))
        if not os.path.exists(dest) or overwrite is True:
            try:
                with open(dest, 'wb') as f:
                    self.retrbinary("RETR {0}".format(name), f.write)
                cprint("[warning]the file {0} has been donwloaded successfully[/warning]".format(dest))
            except FileNotFoundError:
                cprint("[fail]Failed to download the file {0}[/fail]".format(dest))
        else:
            print("Already exists: {0}".format(dest))

    def download_tree(self, path, overwrite=False):
        path = path.lstrip("/")
        original_directory = os.getcwd()
        self.mirror_dir(path, overwrite)
        os.chdir(original_directory)

    def mirror_dir(self, name, overwrite):
        for item in self.nlst(name):
            if self.is_dir(item): # if it is a directory then we don't care
                self.mirror_dir(item, overwrite)
            else:
                self.download_file(item, item, overwrite)

    def create_file(self, path):
        try:
            self.storbinary('STOR {}'.format(path), io.BytesIO(b''))
            return 0
        except:
            return 1

    def create_directory(self, path):
        try:
            if path[0] != "/" and path[0] != ".":
                path = "{}/{}".format(self.pwd(), path)
            self.mkd(path)
            return 0
        except :
             return 1

    def abspath(self, path):
        return sabspath(self, path)

    def ls_info(path):
        """
        Recupere les donnees de chaque entree de la liste
        """
        path = self.abspath(path)
        info = {}
        with Capture() as output:
            self.dir(path)
        if output == "":
            return {}
        for line in output:
            line = line.split()
            file = line[len(line) - 1]
            isdir = line[0][0] == "d"
            line[0] = line[0][1:]
            info[file] = {
                "type": "dir" if isdir else "file",
                "chmod": line[0],
                "hardlinks" : line[1],
                "size" : line[4],
                "modified": " ".join(line[5:-1]),
                "name": file
            }
        return info
