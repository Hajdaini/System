#coding:utf-8

class ls:
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        self.args = args
        self.ftp = ftp
        self.address = address
        self.user = user

    def call(self):
        try:
            file = "{}/{}".format(ftp.pwd(), args[1])
            print(file)
            ftp.mkd(file)
        except :
            print("You may not have permission to create folder")
