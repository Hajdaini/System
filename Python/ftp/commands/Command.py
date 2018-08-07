#coding:utf-8

class Command:
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        self.argc = len(args)
        self.argv = args
        self.ftp = ftp
        self.address = address
        self.user = user
