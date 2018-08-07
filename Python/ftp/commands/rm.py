#coding:utf-8

from commands.Command import Command

class rm(Command):
    def __init__(self, args, ftp, address, user):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        try:
            file1 = "{}/{}".format(self.ftp.pwd(), self.argv[1])
            file2 = "{}/{}".format(self.ftp.pwd(), self.argvv[2])
            if self.argv[1] == '-d' or self.argv[1] == '-D':
                self.ftp.rmd(file2)
            else:
                self.ftp.delete(file1)
        except :
            print("You may not have permission to delete file or folder")
