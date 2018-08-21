#coding:utf-8

import sys, ftplib
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
            return ("connected", self.ftp)
        except ftplib.all_errors as e:
            return ("failed", e)

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
