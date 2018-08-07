#coding:utf-8

class cd:
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        self.argc = len(args)
        self.argv = args
        self.ftp = ftp
        self.address = address
        self.user = user

    def call(self):
        try:
            self.ftp.sendcmd('CWD {}'.format(self.argv[1]))
        except:
            print('Directory may not exist or you may not have permission to view it.')
