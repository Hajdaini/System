#coding:utf-8

from modules.Command import Command
from modules.color import error, success, info
import random, string, os

class get(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        try:
            file = "{}/{}".format(self.ftp.pwd(), self.argv[1])
            info("Downloading ...")
            if self.ftp.is_dir(file):
                self.ftp.download_tree(file)
            else:
                random_filename = (''.join(random.choice(string.ascii_lowercase) for _ in range(6)))
                self.ftp.retrbinary('RETR ' + self.argv[1], open(random_filename, 'wb').write)
                real_filename = self.argv[1].replace("\\", "/").split("/")[-1]
                os.rename(random_filename, real_filename)
            success('Download success !\n')
        except :
            error('File may not exist or you may not have permission to view it.')
