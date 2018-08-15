# coding:utf-8

from modules.Command import Command
from modules.color import error
import time

class put(Command):
    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        start_time = time.time()
        self.ftp.push(self.argv[1])
        print("Finish in {0:.4f} s".format(time.time() - start_time))
