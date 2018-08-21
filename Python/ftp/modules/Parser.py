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
                self.execute(shlex.split(seq))
            except ConnectionAbortedError:
                fatal("Une connexion établie a été abandonnée par un logiciel de votre ordinateur hôte")

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

    def _call(self, cmd):
        """
        Appelle une commande sans protection
        """
        PKG = importlib.import_module("commands.{}".format(cmd[0]))
        cls = getattr(PKG, cmd[0])
        cls = cls(cmd, self.ftp)
        cls.call()
        self.ftp = cls.ftp
