#coding:utf-8

import re
from commands.Command import Command
from modules.color import *


class df(Command):
    def __init__(self, args, ftp, address, user):
        Command.__init__(self, args, ftp, address, user)

    
    def byte_convert(self, n):
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.1f%s' % (value, s)
        return "%sB" % n

    def get_total_size(self, directory):
        size = 0
        for file in self.ftp.nlst(directory):
            size += self.ftp.size(file)
        size = self.byte_convert(size)
        return size


    def call(self):
        try:
            #
            if len(self.argv) == 2:
                print("{} : {}".format(self.argv[1], self.get_total_size(self.argv[1])))
            elif len(self.argv) == 1:
                ls = []
                self.ftp.retrlines('MLSD', ls.append)
                for entry in ls:
                    name = entry.split(";")[-1].lstrip()
                    r1 = re.findall(r"type=(file|dir)", entry)
                    type = ''.join(r1)
                    if type == "dir":
                        cprint("[blue]{}[/blue] : {}".format(name, self.get_total_size(name)))
                    else:
                        print("{} : {}".format(name, self.byte_convert(self.ftp.size(name))))
            else:
                error('[Error] : df or df <folder>')
        except :
            warning('File or Folder may not exist or you may not have permission to access it.')
