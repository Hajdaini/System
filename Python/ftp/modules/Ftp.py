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
        self.chome = None
        self.debug = False
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
        test = path.split("/")[-1]
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
        lst = self.nlst(path)
        info = {}
        with Capture() as output:
            self.dir(path)
        if output == "":
            return {}
        for idx, line in enumerate(output):
            file = lst[idx].split("/")[-1]
            line = line[0:(len(file) * -1)].split()
            isdir = line[0][0] == "d"
            line[0] = line[0][1:]
            info[file] = {
                "type": "dir" if isdir else "file",
                "chmod": line[0],
                "hardlinks": line[1],
                "size": line[4],
                "modified": " ".join(line[5:]),
                "name": file
            }
        return info

    # ------------------------------------------------------------
    # DATA TRANSFERS
    # ------------------------------------------------------------

    def pull(self, srcpath="./", destpath="./", overwrite=False, depth=0):
        """
        Telecharge une arborescence de fichiers du serveur
        """
        if srcpath[-1] == "/":
            srcpath = srcpath[0:-1]
        srcpath = self.sabspath(srcpath)
        destpath = self.cabspath(destpath)
        self.create_tree(destpath, True)
        destpath = self.abspath(destpath, srcpath.split("/")[-1])
        if not self.exists(srcpath):
            return warning("Remote file not exists: " + srcpath)
        elif Path(destpath).is_file() and overwrite is False:
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
                try:
                    os.makedirs(destpath)
                except:
                    return warning("Failed to create local directory: " + destpath)
            ls = self.nlst(srcpath)
            for el in ls:
                el = el.split("/")[-1]
                src = self.abspath(srcpath, el)
                dest = self.abspath(destpath, el)
                self.pull(src, dest, overwrite)

    def push(self, srcpath="./", destpath="./", overwrite=False):
        """
        Envoie une arborescence de fichiers au serveur
        """
        if srcpath[-1] == "/":
            srcpath = srcpath[0:-1]
        srcpath = self.cabspath(srcpath)
        destpath = self.sabspath(destpath)
        self.create_tree(destpath)
        destpath = self.abspath(destpath, srcpath.split("/")[-1])
        if not Path(srcpath).exists():
            return warning("Local file not exists: " + srcpath)
        elif self.is_file(destpath) and overwrite is False:
            return warning("Remote file already exists: " + destpath)
        if Path(srcpath).is_file():
            try:
                file = open(srcpath, "rb")
                try:
                    self.storbinary("STOR /" + destpath, file)
                except:
                    return warning("Transfer failed: " + srcpath)
                file.close()
            except:
                return warning("Could not acceess local file: " + srcpath)
        elif Path(srcpath).is_dir():
            if not self.exists(destpath):
                try:
                    self.mkd(destpath)
                except:
                    return warning("Failed to create remote directory: " + destpath)
            ls = os.listdir(srcpath)
            for el in ls:
                src = self.abspath(srcpath, el)
                dest = self.abspath(destpath, el)
                self.push(src, dest, overwrite)

    def create_tree(self, path="./", local=False):
        if local:
            path = self.cabspath(path)
            if not Path(path).exists():
                os.makedirs(path)
        else:
            path = self.sabspath(path)
            parent = "/".join(path.split("/")[0:-1])
            if not self.exists(parent):
                self.create_tree(parent)
            self.mkd(path)

    # ------------------------------------------------------------
    # PATHS DEFINITION
    # ------------------------------------------------------------

    def cabspath(self, path="./"):
        """
        Recompose un chemin absolu a partir de la position sur le terminal client
        """
        path = path.replace("\\", "/")
        try:
            pwd = self.chome
            return self.abspath(pwd, path)
        except:
            return ""

    def sabspath(self, path="./"):
        """
        Recompose un chemin absolu a partir de la position sur le yrtminal serveur
        """
        path = path.replace("\\", "/")
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
        isroot = True if pwd[0] == "/" else False
        if path[0] == "/":
            return path
        pwd = self._trim(pwd.split("/"))
        cpath = path.split("/")
        for idx, el in enumerate(path.split("/")):
            if el == ".." or el == ".":
                del cpath[0]
                if el == ".." and len(pwd):
                    pwd.pop()
            else:
                break
        path = "{}/{}".format("/".join(pwd), "/".join(cpath))
        return "/" + path if isroot else path

    def _trim(self, lst):
        for idx, el in enumerate(lst):
            if el == "":
                del lst[0]
            if lst[-1] == "":
                del lst[-1]
        return lst

    def _escape(self, path):
        path = path.split("/")
        for idx, el in enumerate(path):
            if " " in el:
                path[idx] = "'{}'".format(el)
        return "/".join(path)
