#coding:utf-8

from commands.Command import Command

class get(Command):
    def __init__(self, args, ftp, address, user):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        try:
            file = "{}/{}".format(self.ftp.pwd(), self.argv[1])
            print("Downloading ...")
            if self.ftp.is_dir(file):
                self.ftp.download_tree(file)
            else:
                self.ftp.retrbinary('RETR ' + self.argv[1], open(self.argv[1], 'wb').write)
            print('Download success !')
        except :
            print('File may not exist or you may not have permission to view it.')
