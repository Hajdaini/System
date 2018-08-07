#coding:utf-8

class ls:
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        self.args = args
        self.ftp = ftp
        self.address = address
        self.user = user

    def call(self):
        try:
            file1 = "{}/{}".format(ftp.pwd(), args[1])
            file2 = "{}/{}".format(ftp.pwd(), args[2])
            if args[1] == '-d' or args[1] == '-D':
                ftp.rmd(file2)
            else:
                ftp.delete(file1)
        except :
            print("You may not have permission to delete file or folder")
