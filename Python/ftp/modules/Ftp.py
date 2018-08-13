# coding:utf-8

import io, re, os
from ftplib import FTP
from pathlib import Path
from modules.color import *
from modules.Capture import Capture


# Table of contents
#   - FILESYSTEM TESTS
#   - FILESYSTEM INSPECTION
#   - DATA TRANSFERS
#   - PATHS DEFINITION

class Ftp(FTP):
    def __init__(self, address="127.0.0.1", user="anonymous", port=21, timeout=30):
        FTP.__init__(self, address, timeout=timeout)
        self.home = None
        self.address = address
        self.user = user
        self.port = port

    # ------------------------------------------------------------
    # FILESYSTEM TESTS
    # ------------------------------------------------------------

    def is_empty(self, path="./"):
        """
        Verifie si un dossier distant est vide
        """
        path = self.sabspath(path)
        if not self.exists(path) or self.is_file(path):
            return False
        with Capture() as output:
            self.dir(path)
        return len(output) == 0

    def is_dir(self, path="./"):
        """
        Verifie si le fichier distant est un dossier
        """
        path = self.sabspath(path)
        if len(path) == 1 and path[0] == "/":
            return True
        test = path.split("/")
        test = test[len(test) - 1]
        path = self.abspath(path, "../")
        ls = self.ls_info(path)
        return test in ls and ls[test]["type"] == "dir"

    def is_file(self, path="./"):
        """
        Verifie si le fichier distant est un fichier regulier
        """
        path = self.sabspath(path)
        if len(path) == 1 and path[0] == "/":
            return False
        test = path.split("/")
        test = test[len(test) - 1]
        path = self.abspath(path, "../")
        ls = self.ls_info(path)
        return test in ls and ls[test]["type"] == "file"

    def exists(self, path="./"):
        """
        Verifieifie si le fichier distant existe
        """
        path = self.sabspath(path)
        if len(path) == 1 and path[0] == "/":
            return False
        test = path.split("/")
        test = test[len(test) - 1]
        path = self.abspath(path, "../")
        ls = self.ls_info(path)
        return test in ls

    # ------------------------------------------------------------
    # FILESYSTEM INSPECTION
    # ------------------------------------------------------------

    def get_tree(self, path="./"):
        path = self.sabspath(path)
        tree = []
        for file in self.nlst():
            if self.is_file(file):
                tree.append(self.abspath(path, file))
            else:
                branch = self.get_tree(path)
                tree.append({self.abspath(path, file): branch})
        return tree

    def ls_info(self, path="./"):
        """
        Recupere les donnees de chaque entree de la liste
        """
        path = self.sabspath(path)
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
                "hardlinks": line[1],
                "size": line[4],
                "modified": " ".join(line[5:-1]),
                "name": file
            }
        return info

    # ------------------------------------------------------------
    # DATA TRANSFERS
    # ------------------------------------------------------------

    def pull(self, srcpath="./", destpath=None, overwrite=False, depth=0):
        """
        Telecharge une arborescence de fichiers du serveur
        """
        destpath = destpath.replace('\\', '/')
        if destpath is None:
            destpath = srcpath.split("/")[-1]
        srcpath = self.sabspath(srcpath)
        if not self.exists(srcpath):
            return warning("Remote file not exists: " + srcpath)
        elif Path(destpath).exists() and overwrite is False:
            return warning("Local file already exists: " + destpath)
        if self.is_file(srcpath):
            try:
                destfile = open(destpath, "wb")
                try:
                    self.retrbinary("RETR " + srcpath, destfile.write)
                except:
                    error("File transfer failed: " + srcpath)
                destfile.close()
            except:
                error("File transfer failed: " + srcpath)
        elif self.is_dir(srcpath):
            if not Path(destpath).exists():
                os.makedirs(destpath)
            ls = self.nlst(srcpath)
            for el in ls:
                el = el.split("/")[-1]
                src = self.abspath(srcpath, el)
                dest = self.abspath(destpath, el)
                if self.is_dir(src):
                    if not Path(dest).exists():
                        os.makedirs(dest)
                self.pull(src, dest, overwrite, depth + 1)

    def push(self, srcpath="./", destpath=None, overwrite=False):
        """
        Envoie une arborescence de fichiers au serveur
        """
        srcpath = srcpath.replace('\\', '/')
        if destpath == None:
            destpath = srcpath.split("/")[-1]
        destpath = self.sabspath(destpath)
        if not Path(srcpath).exists():
            return warning("Local file not exists: " + srcpath)
        elif self.exists(destpath) and overwrite is False:
            return warning("Remote file already exists: " + destpath)
        if Path(srcpath).is_file():
            try:
                srcfile = open(srcpath, "rb")
                try:
                    self.storbinary("STOR " + destpath, srcfile)
                except:
                    error("File transfer failed: " + srcpath)
                srcfile.close()
            except:
                error("File transfer failed: " + srcpath)
        elif Path(srcpath).is_dir():
            if not self.exists(destpath):
                self.mkd(destpath)
            ls = os.listdir(srcpath)
            for el in ls:
                src = self.abspath(srcpath, el)
                dest = self.abspath(destpath, el)
                if Path(src).is_dir():
                    if not self.exists(dest):
                        self.mkd(dest)
                self.push(src, dest, overwrite)

    # ------------------------------------------------------------
    # PATHS DEFINITION
    # ------------------------------------------------------------

    def cabspath(self, path="./"):
        """
        Recompose un chemin absolu a partir de la position sur le terminal client
        """
        if path[0] == "~":
            return str(Path.home()) + path[1:]
        try:
            pwd = str(Path.home())
            return self.abspath(pwd, path)
        except:
            return ""

    def sabspath(self, path="./"):
        """
        Recompose un chemin absolu a partir de la position sur le yrtminal serveur
        """
        if path[0] == "~":
            return self.home + path[1:]
        try:
            pwd = self.pwd()
            return self.abspath(pwd, path)
        except:
            return ""

    def abspath(self, pwd, path):
        """
        Recompose un chemin absolu a partir de deux chaines quelconques
        """
        if path[0] == "/":
            return path
        pwd = pwd.split("/")
        del pwd[0]
        cpath = path.split("/")
        for idx, el in enumerate(path.split("/")):
            if el == ".." or el == ".":
                del cpath[0]
                if el == ".." and len(pwd):
                    pwd.pop()
            else:
                break
        if len(pwd):
            pwd[0] = "/{}".format(pwd[0])
        return "{}/{}".format("/".join(pwd), "/".join(cpath))
