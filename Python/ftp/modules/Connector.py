# coding:utf-8

import ftplib
import sys, os
from getpass import getpass

from modules.Config import Config
from modules.Ftp import Ftp
from modules.color import cprint, error, fatal, success


class Connector:
    """
    Gere la connexion au serveur
    """

    def __init__(self):
        data = Config.load()
        self.address = data['address']
        self.user = data['user']
        self.password = ""
        self.port = int(data['port'])
        self.timeout = int(data['timeout'])
        self.ftp = None
        self.debug = False

    def attempt(self):
        """
        Lance l'interface de connexion manuelle
        """
        state = "idle"
        Config.display_config(show=['user', 'address', 'port', 'timeout'])
        while state != "connected":
            if state == "failed":
                error("FTP failed to connect: {}".format(res))
            try:
                tmp = getpass("FTP Password: ")
                self.password = tmp if tmp != "" else self.password
            except KeyboardInterrupt:
                cprint("\n[b]Good Bye {}![/b]".format(self.user))
                sys.exit(1)
            state, res = self.connect()
        self.config()
        self.welcome()

    def connect(self):
        """
        Tente de se connecter
        """
        try:
            self.ftp = Ftp(self.address, self.user, self.port, self.timeout)
            self.ftp.connect(self.address, self.port)
            self.ftp.login(self.user, self.password)
            if Config.is_prot_d() is True:
                self.ftp.prot_p()
            self.test_prot_d()
            return ("connected", self.ftp)
        except ftplib.all_errors as e:
            e = str(e)
            print("\n")
            error(e + "\n")
            if 'TLS' in e or 'plain' in e:
                cprint(
                    "[b]Solution[/b]: Change the \"[b][blue]ftps[/blue][/b]\" options to "
                    "\"[b][green]true[/green][/b]\" in \"[warning]{}[/warning]\"\n".format(
                        Config.get_config_path_for_print_only()))
            elif 'incorrect' in e or 'password' in e:
                cprint(
                    "[b]Solution[/b]: Be sure to have the right \"[b][blue]address[/blue][/b]\","
                    " \"[b][blue]address[/blue][/b]\","
                    " \"[b][blue]user[/blue][/b]\" and"
                    " \"[b][blue]port[/blue][/b]\""
                    " in \"[warning]{}[/warning]\"\n".format(
                        Config.get_config_path_for_print_only()))
            sys.exit(1)

    def test_prot_d(self):
        try:
            sys.stdout = open(os.devnull, 'w')
            self.ftp.retrlines('LIST')
            sys.stdout = sys.__stdout__
        except:
            print("\n")
            error("PROT P required\n")
            cprint(
                "[b]Solution[/b]: Change the \"[b][blue]prot_d[/blue][/b]\" options to \"[b][green]true[/green][/b]\" in \"[warning]{}[/warning]\"\n".format(
                    Config.get_config_path_for_print_only()))
            sys.exit(1)

    def config(self):
        """
        Definit la configuration de base du serveur
        """
        try:
            self.ftp.encoding = 'utf-8'
            self.ftp.home = self.ftp.pwd()
            self.ftp.set_debuglevel(2 if self.debug == True else 0)
        except:
            fatal("Cannot go further")
            sys.exit(1)

    def welcome(self):
        """
        Affiche le message de bienvenue du serveur
        """
        try:
            success("You are now connected to server")
            cprint("\n[b]Welcome {}![/b] I am:\n{}\n".format(self.user, self.ftp.getwelcome()))
        except:
            fatal("Cannot go further")
            sys.exit(1)
