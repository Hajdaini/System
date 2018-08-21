# coding:utf-8

import importlib
import shlex
import sys
from modules.Capture import Capture
from modules.color import *


class Parser:
    def __init__(self, ftp):
        self.ftp = ftp
        self.debug = 0

    def split(self, str):
        """
        Decompose la sequence de commandes
        """
        return shlex.split(str)

    def watch(self):
        """
        Attend une sequence de commandes de l'entree standard
        """
        while True:
            try:
                try:
                    seq = cinput(
                        "[b][green]ftp://{}@{}:[blue]{}[/endc][b]$>[/endc] ".format(self.ftp.user, self.ftp.address,
                                                                                    self.ftp.pwd()))
                except KeyboardInterrupt:
                    cprint("\n[b]Good Bye {}![/b]".format(self.ftp.user))
                    sys.exit(1)
                if seq == "":
                    continue
                self.dispatch(seq)
            except ConnectionAbortedError:
                fatal("Une connexion établie a été abandonnée par un logiciel de votre ordinateur hôte")

    def dispatch(self, str):
        """
        Abalyse la sequence decomposee, recree les commandes et les execute
        """
        cmd = []
        stdin = []
        seq = self.split(str)
        slen = len(seq)
        prevredir = None
        found_std = 0
        for idx, el in enumerate(seq):
            if self.is_std(el):
                found_std = 1
            if not self.is_redir(el) and not self.is_std(el) and not found_std:
                cmd.append(el)
            if el == "<":
                try:
                    cmd = self.read_file(seq[idx + 1])
                except:
                    warning("File not found")
                    break
            if el == ">":
                try:
                    cmd = self.write_file(cmd, seq[idx + 1])
                except:
                    warning("File not found")
                    break
            if el == ">>":
                try:
                    cmd = self.concat_file(cmd, seq[idx + 1])
                except:
                    warning("File not found")
                    break
            elif el == "<<":
                try:
                    cmd = self.read_stdin(seq[idx + 1])
                except:
                    warning("Cannot read from stdin")
                    break
            if self.is_redir(el) or idx == slen - 1:
                # print(cmd)
                if prevredir != None and prevredir in "|":
                    cmd = [cmd[0], "\n".join(stdin)]
                # print(cmd)
                if el in "|":
                    with Capture() as stdin:
                        self.execute(cmd)
                else:
                    self.execute(cmd)
                cmd = []
                if self.is_redir(el):
                    prevredir = el
            if self.is_redir(el) or idx == slen - 1:
                prevredir = None if idx == slen - 1 else el

    def execute(self, cmd):
        """
        Lance l'appel d'une commande

        Debug True: Appel non protege
        Debug False: Appel protege
        """
        if self.debug:
            self._call(cmd)
        else:
            try:
                self._call(cmd)
            except:
                warning("Command {} not found. Type help to get available commands".format(cmd[0]))

    def is_redir(self, el):
        """
        Definit si un element de la sequence de commandes correspond a un lien ()&, |
        """
        return el in "&" or el in "|"

    def is_std(self, el):
        return el in ">" or el in "<" or el in "<<" or el in ">>"

    def read_stdin(self, stop):
        cmd = ""
        tmp = None
        while tmp != stop:
            tmp = input("> ")
            if tmp != stop:
                cmd = "{}{}".format(cmd, tmp)
        return cmd

    def read_file(self, path):
        return self.ftp.read_file(path)

    def write_file(self, path, data):
        self.ftp.write_file(path, data)

    def concat_file(self, path, data):
        text = self.read_file(path)
        self.write_file(path, "{}{}".format(text))

    def _call(self, cmd):
        """
        Appelle une commande sans protection
        """
        PKG = importlib.import_module("commands.{}".format(cmd[0]))
        cls = getattr(PKG, cmd[0])
        cls = cls(cmd, self.ftp)
        cls.call()
        self.ftp = cls.ftp
