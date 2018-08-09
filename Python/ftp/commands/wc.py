#coding:utf-8

import os
from commands.Command import Command
from modules.color import error

class wc(Command):
    def __init__(self, args, ftp, address, user):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        try:
            filename = self.argv[1]
            with open(filename, 'wb') as file:
                self.ftp.retrbinary('RETR %s' % filename, file.write)

            with open(filename, 'r') as file:
                num_lines = sum(1 for line in file)
                print("number of lines :", num_lines)

                file.seek(0, 0)
                wordcounter = 0
                for line in file:
                    wordcounter += len(line.split())
                print("number of words :", wordcounter)

                file.seek(0, 0)
                print("number of characters :", len(file.read()))

            os.remove(filename)
        except:
            error('File may not exist or you may not have permission to access it.')
