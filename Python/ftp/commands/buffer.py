#coding:utf-8

from commands.Command import Command

class buffer(Command):
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        Command.__init__(self, args, ftp, address, user)
        self.buffer = ""

    def call(self):
        path = self.ftp.abspath(self.argv[1])
        self.ftp.retrlines("RETR " + path, self.get_buffer)
        print(self.buffer)

    def get_buffer(self, str=""):
        self.buffer = self.buffer + str
