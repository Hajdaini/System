#coding:utf-8

from commands.Command import Command

class cat(Command):
    def __init__(self, args, ftp, address, user):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        try:
            file = "{}/{}".format(self.ftp.pwd(), self.argv[1])
            with open(file, "r") as file:
                print(file.read())
        except :
            print('File may not exist or you may not have permission to access it.')
