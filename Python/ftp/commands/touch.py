#coding:utf-8
import io

from commands.Command import Command

class touch(Command):
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        try:
            self.ftp.storbinary('STOR {}'.format(self.argv[1]), io.BytesIO(b''))
        except e:
            print('Directory may not exist or you may not have permission to view it. ' e)
