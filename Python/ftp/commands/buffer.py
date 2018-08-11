#coding:utf-8

from commands.Command import Command
from modules.Capture import Capture

class buffer(Command):
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        path = self.ftp.abspath(self.argv[1])
        with Capture() as stdout:
            self.ftp.retrlines("RETR " + path, print)
        print(str("".join(stdout)))
