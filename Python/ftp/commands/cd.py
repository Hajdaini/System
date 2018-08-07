#coding:utf-8

from commands.Command import Command

class cd(Command):
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        try:
            self.ftp.sendcmd('CWD {}'.format(self.argv[1]))
        except:
            print('Directory may not exist or you may not have permission to view it.')