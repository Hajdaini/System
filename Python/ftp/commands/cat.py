#coding:utf-8

class cat:
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        self.argc = len(args)
        self.argv = args
        self.ftp = ftp
        self.address = address
        self.user = user

    def call(self):
        try:
            file = "{}/{}".format(self.ftp.pwd(), self.argv[1])
            with open(file, "r") as file:
                print(file.read())
        except :
            print('File may not exist or you may not have permission to access it.')
