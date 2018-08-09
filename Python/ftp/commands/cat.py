#coding:utf-8

import os
from commands.Command import Command
from modules.color import error

class cat(Command):
    def __init__(self, args, ftp, address, user):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        #try:
        filename = self.ftp.abspath(self.argv[1])
        print(filename)
        """
        with open(filename, 'wb') as file:
            self.ftp.retrbinary('RETR %s' % filename, file.write)
        with open(filename, 'r') as file:
            print(file.read())
        os.remove(filename)
        """
        #except:
            #error('File may not exist or you may not have permission to access it.')
