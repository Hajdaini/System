#coding:utf-8

import sys
import ftplib
from getpass import getpass
from modules.Ftp import Ftp
from modules.color import cprint, error, fatal, success

class Connector:
    """
    Gere la connexion au serveur
    """
    def __init__(self, address="127.0.0.1", user="anonymous", password="", port=21, timeout=30):
        self.address = address
        self.user = user
        self.password = password
        self.port = int(port)
        self.timeout = int(timeout)
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
                tmp = input("FTP Host ({}): ".format(self.address))
                self.address = tmp if tmp != "" else self.address

                tmp = input("FTP User ({}): ".format(self.user))
                self.user = tmp if tmp != "" else self.user

                tmp = getpass("FTP Password: ")
                self.password = tmp if tmp != "" else self.password

                tmp = input("FTP Port ({}): ".format(self.port))
                self.port = int(tmp) if tmp != "" else self.port

                tmp = input("FTP Connection Timeout ({} seconds): ".format(self.timeout))
                self.timeout = int(tmp) if tmp != "" else self.timeout
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
            self.ftp = Ftp(self.address, self.timeout)
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
