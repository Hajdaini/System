#coding:utf-8

import io, re, os
from modules.color import *
from ftplib import FTP
from pathlib import Path
from modules.path import *
from modules.Capture import Capture

class Ftp(FTP):
    def __init__(self, host="127.0.0.1", timeout=30):
        FTP.__init__(self, host, timeout=timeout)
        self.home = None

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
                ftp.retrbinary("RETR " + srcpath, destfile.write)
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
        srcpath = self.abspath(srcpath)
        destpath = cabspath(destpath)
        if not overwrite and self.exists(destpath):
            warning("Remote file already exists: " + destpath)
            return
        try:
            srcfile = open(srcpath, "rb")
            try:
                ftp.storbinary("STOR " + destpath, srcfile)
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

    def pushr(self, srcpath, destpath=None, overwrite=False):
        """
        Envoie une arborescence de fichiers au serveur
        """
        if destpath == None:
            destpath = srcpath
        srcpath = self.abspath(srcpath)
        destpath = cabspath(destpath)
        if Path(srcpath).is_file():
            print(srcpath + " | " + destpath)
            #self.push(srcpath, destpath, overwrite)
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
                    print(src + " | " + dest)
                    self.pushr(src, dest, overwrite)
                else:
                    self.pushr(src, dest, overwrite)

    """
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
    """

    def abspath(self, path):
        """
        Determine un chemin absolu a partir d'un chemin quelconque
        """
        return sabspath(self, path)

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
