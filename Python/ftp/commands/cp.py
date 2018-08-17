# coding:utf-8

from modules.Command import Command
from modules.color import error, info
import time

class cp(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        start_time = time.time()
        self.ftp.pull(self.argv[1], './udload')
        self.ftp.push('./udload/' + self.argv[1], self.argv[2])
        print("Finish in {0:.4f} s".format(time.time() - start_time))
