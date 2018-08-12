#coding:utf-8

import io, re, os
from ftplib import FTP
from pathlib import Path
from modules.color import *
from modules.Capture import Capture

class Ftp(FTP):
    def __init__(self, address="127.0.0.1", user="anonymous", port=21, timeout=30):
        FTP.__init__(self, address, timeout=timeout)
        self.home = None
        self.address = address
        self.user = user
        self.port = port

    def is_empty(self, path):
        """
        Verifie si un dossier distant est vide
        """
        path = self.abspath(path)
        if not self.exists(path) or self.is_file(path):
            return False
        with Capture() as output:
            self.dir(path)
        return len(output) == 0

    def is_dir(self, path="./"):
        """
        Verifie si le fichier distant est un dossier
        """
        path = self.abspath(path)
        if len(path) == 1 and path[0] == "/":
            return True
        test = path.split("/")
        test = test[len(test) - 1]
        path = abspath(path, "../")
        ls = self.ls_info(path)
        return test in ls and ls[test]["type"] == "dir"

    def is_file(self, path):
        """
        Verifie si le fichier distant est un fichier regulier
        """
        path = self.abspath(path)
        if len(path) == 1 and path[0] == "/":
            return False
        test = path.split("/")
        test = test[len(test) - 1]
        path = abspath(path, "../")
        ls = self.ls_info(path)
        return test in ls and ls[test]["type"] == "file"

    def exists(self, path):
        """
        Verifieifie si le fichier distant existe
        """
        path = self.abspath(path)
        if len(path) == 1 and path[0] == "/":
            return False
        test = path.split("/")
        test = test[len(test) - 1]
        path = abspath(path, "../")
        ls = self.ls_info(path)
        return test in ls

    def pull(self, srcpath, destpath=None, pverwrite=False):
        """
        Telecharge un fichier du serveur
        """
        if destpath == None:
            destpath = srcpath
        srcpath = self.abspath(srcpath)
        destpath = cabspath(destpath)
        if not overwrite and Path(destpath).exists():
            warning("Local file already exists: " + destpath)
            return
        try:
            destfile = open(destpath, "wb")
            try:
                self.retrbinary("RETR " + srcpath, destfile.write)
            except:
                error("File transfer failed: " + srcpath)
            destfile.close()
        except:
            error("File transfer failed: " + srcpath)

    def push(self, srcpath, destpath=None, overwrite=False):
        """
        Envoie un fichier au serveur
        """
        if destpath == None:
            destpath = srcpath
        srcpath = cabspath(srcpath)
        destpath = self.abspath(destpath)
        if not overwrite and self.exists(destpath):
            warning("Remote file already exists: " + destpath)
            return
        try:
            srcfile = open(srcpath, "rb")
            try:
                self.storbinary("STOR " + destpath, srcfile)
            except:
                error("File transfer failed: " + srcpath)
            srcfile.close()
        except:
            error("File transfer failed: " + srcpath)

    def pullr(self, srcpath, destpath=None, pverwrite=False):
        """
        Telecharge une arborescence de fichiers du serveur
        """
        if destpath == None:
            destpath = srcpath
        srcpath = self.abspath(srcpath)
        destpath = cabspath(destpath)
        if Path(srcpath).is_file():
            self.push(srcpath, destpath, overwrite)
        elif Path(srcpath).is_dir():
            if not self.exists(destpath):
                self.mkd(destpath)
            ls = os.listdir(srcpath)
            for el in ls:
                src = abspath(srcpath, el)
                dest = abspath(destpath, el)
                if Path(src).is_dir():
                    if not self.exists(dest):
                        self.mkd(dest)
                    self.pushr(src, dest, overwrite)
                else:
                    self.pushr(src, dest, overwrite)

    def pushr(self, srcpath, destpath=None, overwrite=False):
        """
        Envoie une arborescence de fichiers au serveur
        """
        if destpath == None:
            destpath = srcpath
        srcpath = self.abspath(srcpath)
        destpath = cabspath(destpath)
        if Path(srcpath).is_file():
            self.push(srcpath, destpath, overwrite)
        elif Path(srcpath).is_dir():
            if not self.exists(destpath):
                self.mkd(destpath)
            ls = os.listdir(srcpath)
            for el in ls:
                src = abspath(srcpath, el)
                dest = abspath(destpath, el)
                if Path(src).is_dir():
                    if not self.exists(dest):
                        self.mkd(dest)
                    self.pushr(src, dest, overwrite)
                else:
                    self.pushr(src, dest, overwrite)

    def cabspath(self, path):
        """
        Recompose un chemin absolu a partir de la position sur le terminal client
        """
        if path[0] == "~":
            return str(Path.home()) + path[1:]
        try:
            pwd = str(Path.home())
            return self._abspath(pwd, path)
        except:
            return None

    def sabspath(self, path):
        """
        Recompose un chemin absolu a partir de la position sur le yrtminal serveur
        """
        if path[0] == "~":
            return self.home + path[1:]
        try:
            pwd = self.pwd()
            return self._abspath(pwd, path)
        except:
            return None

    def ls_info(self, path):
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

    def _abspath(pwd, path):
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
        if (len(pwd)):
            pwd[0] = "/{}".format(pwd[0])
        return "{}/{}".format("/".join(pwd), "/".join(cpath))
