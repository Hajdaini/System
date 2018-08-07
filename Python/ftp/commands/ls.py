#coding:utf-8

class ls:
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        self.args = args
        self.ftp = ftp
        self.address = address
        self.user = user

    def call(self):
        if len(self.args) == 1:
            self.ftp.dir()
        elif len(self.args) == 2:
            self.ftp.dir(self.args[1])
        else:
            print("Error (Usage : ls <path>)")
