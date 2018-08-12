#coding:utf-8

import random, string

class Command:
    def __init__(self, args, ftp):
        self.argc = len(args)
        self.argv = args
        self.ftp = ftp

    def randstr(size=6):
        return (''.join(random.choice(string.ascii_lowercase) for _ in range(size)))
