#coding:utf-8

import os
from commands.Command import Command
from modules.color import error
import random, string

class cat(Command):
    def __init__(self, args, ftp, address, user):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        try:
            random_filename = (''.join(random.choice(string.ascii_lowercase) for _ in range(6)))
            filename = self.argv[1]
            with open(random_filename, 'wb') as file:
                self.ftp.retrbinary('RETR %s' % filename, file.write)
            with open(random_filename, 'r') as file:
                print(file.read())
            os.remove(random_filename)
        except:
            error('File may not exist or you may not have permission to access it.')
