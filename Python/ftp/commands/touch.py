# coding:utf-8
import io

from modules.Command import Command
from modules.color import error


class touch(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        try:
            for idx, el in enumerate(self.argv):
                if idx:
                    self.ftp.storbinary('STOR {}'.format(el), io.BytesIO(b''))
        except:
            error('Access denied.')
