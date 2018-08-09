#coding:utf-8

from commands.Command import Command

class test(Command):
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        #print(self.ftp.exists(self.argv[1]))
        #print(self.ftp.is_file(self.argv[1]))
        print(self.ftp.is_dir(self.argv[1]))
