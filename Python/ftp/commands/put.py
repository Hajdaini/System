#coding:utf-8

from modules.Command import Command
from modules.color import error

class put(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        try:
            file = "{}/{}".format(self.ftp.pwd(), self.argv[1])
            self.ftp.storbinary('STR {}'.format(self.argv[1]), open(file, 'rb'))
        except :
            error("You may not have permission to upload")
