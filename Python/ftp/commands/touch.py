# coding:utf-8
import io

from modules.Command import Command
from modules.color import error


class touch(Command):
    """
    [b]SYNOPSIS[/b]

        [b]touch[/b]   [u]FILE[/u]

    [b]DESCRIPTION[/b]

        create file
    """

    def __init__(self, args, ftp):
        Command.__init__(self, args, ftp)

    def call(self):
        try:
            for idx, el in enumerate(self.argv):
                if idx:
                    self.ftp.storbinary('STOR {}'.format(el), io.BytesIO(b''))
        except:
            error('Access denied.')
