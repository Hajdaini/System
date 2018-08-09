#coding:utf-8

import io
import os
import re
import os
from modules.color import *
from ftplib import FTP

class Ftp(FTP):
    def __init__(self, host="127.0.0.1", timeout=30):
        FTP.__init__(self, host, timeout=timeout)

    def exists(self, path):
        return self.is_file(path) or self.is_dir(path)

    def is_file(self, name):
        r1 = re.findall(r"type=(file|dir)", self.sendcmd('MLST {}'.format(name)))
        type = ''.join(r1)
        return type == "file"

    def is_dir(self, name):
        name = self.abspath(name)
        r1 = re.findall(r"type=(file|dir)", self.sendcmd('NLST {}'.format(name)))
        type = ''.join(r1)
        return type == "dir"

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
        if path[0] == "/":
            return path
        pwd = self.pwd().split("/")
        del pwd[0]
        cpath = path.split("/")
        for idx, el in enumerate(path.split("/")):
            if el == ".." or el == ".":
                del cpath[0]
                if el == ".." and len(pwd):
                    pwd.pop()
            else:
                break
        if (len(pwd)):
            pwd[0] = "/{}".format(pwd[0])
        return "{}/{}".format("/".join(pwd), "/".join(cpath))
