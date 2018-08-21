# coding:utf-8

import io, re, os
from ftplib import FTP, FTP_TLS
from pathlib import Path
from modules.color import *
from modules.Capture import Capture
from modules.Benchmark import Benchmark as Bench

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
        self.debug = 0
        self.address = address
        self.user = user
        self.port = port
        self.cp_buffer = None

    # ------------------------------------------------------------
    # FILESYSTEM TESTS
    # ------------------------------------------------------------

    def is_empty(self, path="./"):
        """
        Verifie si un dossier distant est vide
        """
        path = self.sabspath(path)
        try:
            self.nlst(path)[0]
            return False
        except:
            return False
        return True

    def is_dir(self, path="./"):
        """
        Verifie si le fichier distant est un dossier
        """
        path = self.sabspath(path)
        if len(path) == 1 and path[0] == "/":
            return True
        parent = self.abspath(path, "../")
        try:
            list = self.nlst(parent)
        except:
            return False
        with Capture() as output:
            self.dir(parent)
        path = path.split("/")[-1]
        for idx, el in enumerate(list):
            if path == el.split("/")[-1] and output[idx][0] == "d":
                return True
        return False

    def is_file(self, path="./"):
        """
        Verifie si le fichier distant est un fichier regulier
        """
        path = self.sabspath(path)
        if len(path) == 1 and path[0] == "/":
            return False
        parent = self.abspath(path, "../")
        try:
            list = self.nlst(parent)
        except:
            return False
        with Capture() as output:
            self.dir(parent)
        path = path.split("/")[-1]
        for idx, el in enumerate(list):
            if path == el.split("/")[-1] and output[idx][0] == "-":
                return True
        return False

    def exists(self, path="./"):
        """
        Verifieifie si le fichier distant existe
        """
        path = self.sabspath(path)
        if len(path) == 1 and path[0] == "/":
            return True
        parent = self.abspath(path, "../")
        try:
            list = self.nlst(parent)
        except:
            return False
        with Capture() as output:
            self.dir(parent)
        path = path.split("/")[-1]
        for idx, el in enumerate(list):
            if path == el.split("/")[-1]:
                return True
        return False

    # ------------------------------------------------------------
    # FILESYSTEM INSPECTION
    # ------------------------------------------------------------

    def get_tree(self, path="./"):
        path = self.sabspath(path)
        tree = []
        for file in self.nlst(path):
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

    def cp(self, srcpath, destpath="./", overwrite=False, _initial=True):
        """
        Copie un fichier ou repertoire d'un endroit du serveur a un autre
        """
        if _initial:
            Bench.mark("start cp")
            srcpath = self.sabspath(srcpath)
            destpath = self.sabspath(destpath)
            if self.is_dir(srcpath):
                self.create_tree(destpath)
            destpath = self.abspath(destpath, srcpath.split("/")[-1])
            if not self.exists(srcpath):
                return warning("Remote file not exists: " + srcpath)
        if self.is_file(destpath) and overwrite == False:
            return warning("Remote file already exists: " + destpath)
        elif self.is_file(srcpath):
            print("{} bytes for file:".format(self.size(srcpath)))
            try:
                cprint("{}...[b][blue]COPYING[/endc]".format(srcpath))
                self.retrbinary("RETR " + srcpath, self.set_cp_buffer)
                self.storbinary("STOR " + destpath, io.BytesIO(self.cp_buffer))
                self.cp_buffer = None
                cprint("{}...[b][green]OK[/endc]".format(srcpath))
            except:
                cprint("{}...[b][fail]FAILED[/endc]".format(srcpath))
        else:
            if not self.exists(destpath):
                try:
                    self.mkd(destpath)
                    if self.debug:
                        cprint("{}...[b][green]OK[/endc]".format(srcpath))
                except:
                    if self.debug:
                        return cprint("{}...[b][fail]FAILED[/endc]".format(srcpath))
                    else:
                        return warning("Failed to create remote directory: " + destpath)
            ls = self.nlst(srcpath)
            for idx, el in enumerate(ls):
                el = el.split("/")[-1]
                src = self.abspath(srcpath, el)
                dest = self.abspath(destpath, el)
                self.cp(src, dest, overwrite, False)
        if _initial:
            info("Elapsed time: {0:.4f}s".format(Bench.elapsed_time("start cp")))

    def set_cp_buffer(self, buf):
        if self.cp_buffer == None:
            self.cp_buffer = buf
        else:
            self.cp_buffer += buf

    def pull(self, srcpath, destpath="./", overwrite=False, _initial=True):
        """
        Telecharge une arborescence de fichiers du serveur
        """
        if _initial:
            Bench.mark("start pull")
            srcpath = self.sabspath(srcpath)
            destpath = self.cabspath(destpath)
            if self.is_dir(srcpath):
                self.create_tree(destpath, True)
            destpath = self.abspath(destpath, srcpath.split("/")[-1])
            if not self.exists(srcpath):
                return warning("Local file not exists: " + srcpath)
        if Path(destpath).is_file() and overwrite is False:
            warning("Remote file already exists: " + destpath)
        elif self.is_file(srcpath):
            try:
                file = open(destpath, "wb")
                try:
                    self.retrbinary("RETR " + srcpath, file.write)
                    if self.debug:
                        cprint("{}...[b][green]OK[/endc]".format(srcpath))
                except:
                    if self.debug:
                        cprint("{}...[b][fail]FAILED[/endc]".format(srcpath))
                    return warning("Transfer failed: " + srcpath)
                file.close()
            except:
                return warning("Could not create remote file: " + destpath)
        else:
            if not Path(destpath).exists():
                try:
                    os.makedirs(destpath)
                    if self.debug:
                        cprint("{}...[b][green]OK[/endc]".format(srcpath))
                except:
                    if self.debug:
                        return cprint("{}...[b][fail]FAILED[/endc]".format(srcpath))
                    else:
                        return warning("Failed to create remote directory: " + destpath)
            ls = self.nlst(srcpath)
            for idx, el in enumerate(ls):
                src = self.abspath(srcpath, el.split("/")[-1])
                dest = self.abspath(destpath, el.split("/")[-1])
                self.pull(src, dest, overwrite, False)
        if _initial:
            info("Elapsed time: {0:.4f}s".format(Bench.elapsed_time("start pull")))

    def push(self, srcpath, destpath="./", overwrite=False, _initial=True):
        """
        Envoie une arborescence de fichiers au serveur
        """
        if _initial:
            Bench.mark("start push")
            srcpath = self.cabspath(srcpath)
            destpath = self.sabspath(destpath)
            if Path(srcpath).is_dir():
                self.create_tree(destpath)
            destpath = self.abspath(destpath, srcpath.split("/")[-1])
            if not Path(srcpath).exists():
                return warning("Local file not exists: " + srcpath)
        if self.is_file(destpath) and overwrite is False:
            warning("Remote file already exists: " + destpath)
        elif Path(srcpath).is_file():
            try:
                file = open(srcpath, "rb")
                try:
                    self.storbinary("STOR /" + destpath, file)
                    if self.debug:
                        cprint("{}...[b][green]OK[/endc]".format(srcpath))
                except:
                    if self.debug:
                        return cprint("{}...[b][fail]FAILED[/endc]".format(srcpath))
                    else:
                        return warning("Transfer failed: " + srcpath)
                file.close()
            except:
                return warning("Could not acceess local file: " + srcpath)
        else:
            if not self.exists(destpath):
                try:
                    self.mkd(destpath)
                    if self.debug:
                        cprint("{}...[b][green]OK[/endc]".format(srcpath))
                except:
                    if self.debug:
                        return cprint("{}...[b][fail]FAILED[/endc]".format(srcpath))
                    else:
                        return warning("Failed to create remote directory: " + destpath)
            ls = os.listdir(srcpath)
            for idx, el in enumerate(ls):
                src = self.abspath(srcpath, el)
                dest = self.abspath(destpath, el)
                self.push(src, dest, overwrite, False)
        if _initial:
            info("Elapsed time: {0:.4f}s".format(Bench.elapsed_time("start push")))

    def create_tree(self, path="./", local=False):
        if len(path) == 1 and path[0] == "/":
            return
        if local:
            path = self.cabspath(path)
            if not Path(path).exists():
                os.makedirs(path)
        else:
            path = self.sabspath(path)
            parent = "/".join(path.split("/")[0:-1])
            if parent == "":
                parent = "/"
            if not self.exists(parent):
                self.create_tree(parent)
            if not self.exists(path):
                self.mkd(path)

    # ------------------------------------------------------------
    # PATHS DEFINITION
    # ------------------------------------------------------------

    def cabspath(self, path="./"):
        """
        Recompose un chemin absolu a partir de la position sur le terminal client
        """
        if self.debug < 0:
            print("CABSPATH: {} {}".format(self.chome, path))
        try:
            return self.abspath(self.chome, path)
        except:
            return ""

    def sabspath(self, path="./"):
        """
        Recompose un chemin absolu a partir de la position sur le yrtminal serveur
        """
        if self.debug < 0:
            print("SABSPATH: {} {}".format(self.pwd(), path))
        try:
            return self.abspath(self.pwd(), path)
        except:
            return ""

    def abspath(self, pwd, path):
        """
        Recompose un chemin absolu a partir de deux chaines quelconques
        """
        path = self._clean_path(path)
        pattern = re.compile(r"^[a-zA-Z0-9_-]+:/")
        #if self.debug < 0:
        #    print("1 {} => {}".format(pwd, path))
        if len(path) and path[0] == "/":
            return path
        elif os.name == "nt" and pattern.search(path):
            return path
        #if self.debug < 0:
        #    print("2 {} => {}".format(pwd, path))
        pwd = pwd.split("/")
        path = path.split("/")
        #if self.debug < 0:
        #    print("3 {} => {}".format(pwd, path))
        while len(path) and (".." == path[0] or "." == path[0]):
            if len(pwd) > 1 and ".." == path[0]:
                del pwd[-1]
                del path[0]
            else:
                del path[0]
        #if self.debug < 0:
        #    print("4 {} => {}".format(pwd, path))
        if len(path) == 0:
            if len(pwd) == 1 and "/" not in pwd[0]:
                return pwd[0] + "/"
            else:
                return "/".join(pwd)
        if len(pwd) == 1 or (len(pwd) > 1 and len(pwd[-1]) and pwd[-1][-1] != "/"):
            pwd[-1] += "/"
        #if self.debug < 0:
        #    print("5 {} => {}".format(pwd, path))
        return "{}{}".format("/".join(pwd), "/".join(path))

    # ------------------------------------------------------------
    # UTILITIES
    # ------------------------------------------------------------

    def _clean_path(self, path):
        pattern = re.compile(r"^[a-zA-Z0-9_-]+:$")
        path = path.replace(os.path.sep, "/")
        while len(path) > 1 and path[-1] == "/":
            path = path[0:-1]
        if os.name == "nt" and pattern.search(path):
            path += "/"
        return path

class Ftp_TLS(Ftp, FTP_TLS):
    def __init__(self, address="127.0.0.1", user="anonymous", port=21, timeout=30):
        Ftp.__init__(self, address, timeout=timeout)
        Ftp_TLS.__init__(self, address, timeout=timeout)
