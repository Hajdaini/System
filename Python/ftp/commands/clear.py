#coding:utf-8
import os

from modules.Command import Command

class clear(Command):
    def __init__(self,rgs, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
       os.system('cls' if os.name=='nt' else 'clear')
