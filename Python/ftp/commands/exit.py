#coding:utf-8

class exit:
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        self.args = args
        self.ftp = ftp
        self.address = address
        self.user = user

    def call(self):
        print("Good Bye {}!".format(self.user if self.user != "" else "Anonymous"))
