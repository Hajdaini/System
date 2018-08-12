#coding:utf-8

class Command:
    def __init__(self, args, ftp):
        self.argc = len(args)
        self.argv = args
        self.ftp = ftp
        self.address = self.ftp.address
        self.user = self.ftp.user
        self.util = []
