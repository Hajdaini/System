#coding:utf-8
import io

from commands.Command import Command
from modules.color import error

class touch(Command):
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        try:
            for idx, el in enumerate(self.argv):
                if idx:
                    self.ftp.storbinary('STOR {}'.format(el), io.BytesIO(b''))
        except:
            error('Access denied.')
