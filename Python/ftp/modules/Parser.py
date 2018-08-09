#coding:utf-8

import sys
import shlex
import importlib
from modules.Capture import Capture
from modules.color import cprint, warning, cinput

class Parser:
    def __init__(self, ftp, address, user):
        self.ftp = ftp
        self.address = address
        self.user = user
        self.debug = False

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
                seq = cinput("[b][green]ftp://{}@{}:[blue]{}[/endc][b]$>[/endc] ".format(self.user, self.address, self.ftp.pwd()))
            except KeyboardInterrupt:
                cprint("\n[b]Good Bye {}![/b]".format(user))
                sys.exit(1)
            if seq == "":
                continue
            self.dispatch(seq)

    def dispatch(self, str):
        """
        Abalyse la sequence decomposee, recree les commandes et les execute
        """
        cmd = []
        stdin = None
        seq = self.split(str)
        slen = len(seq)
        for idx, el in enumerate(seq):
            if idx and seq[idx - 1] == "&":
                stdin = None
            if el != "&" and el != "|":
                cmd.append(el)
            if el == "&" or el == "|" or idx == slen - 1:
                clen = len(cmd)
                if idx - clen and seq[idx - clen] == "|":
                    stdin = "\n".join(stdin)
                    cmd = [cmd[0], stdin]
                print(cmd)
                with Capture() as stdin:
                    self.execute(cmd)
                if (idx - clen and seq[idx - clen] == "&") or idx == slen - 1:
                    for str in stdin:
                        cprint(str)
                if cmd[0] == "exit":
                    sys.exit(1)
                cmd = []

    def execute(self, cmd):
        """
        Lance l'appel d'une commande

        Debug True: Appel non protege
        Debug False: Appel protege
        """
        if self.debug == True:
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
        cls = cls(cmd, self.ftp, self.address, self.user)
        cls.call()
        self.ftp = cls.ftp
