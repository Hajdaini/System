# coding:utf-8

from modules.Command import Command
from modules.color import *
import time

class cp(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        print('Begin cp, please wait ...')
        start_time = time.time()
        self.ftp.pull(self.argv[1], './udload')
        print('Pull is finish now we push, please wait ...')
        self.ftp.push('./udload/' + self.argv[1], self.argv[2])
        print("Finish in {0:.4f} s".format(time.time() - start_time))
