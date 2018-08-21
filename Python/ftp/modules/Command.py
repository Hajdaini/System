# coding:utf-8
from modules.color import error, warning, fatal
from modules.Loader import Loader

class Command:
    def __init__(self, args, ftp):
        self.argc = len(args)
        self.argv = args
        self.ftp = ftp
        self.address = self.ftp.address
        self.user = self.ftp.user
        self.util = Loader().load("utils")

    def input_error_handle(self, funtion_2_args, funtion_3_args, type_to_verify='both', used_alone=False,
                           used_alone_with_options=False,
                           function_alone=None, function_with_only_option=None):
        type_errors = {"both": "Directory or file missing", "dir": "Directory missing", "file": "File missing"}
        if self.argc == 1:
            if used_alone == False:
                if type_to_verify in type_errors:
                    warning(type_errors[type_to_verify])
                else:
                    fatal('wrong type x259545')
                return True
            else:
                function_alone()
        elif self.argc == 2:
            if self.argv[1][0] == "-" and used_alone_with_options is True:
                function_with_only_option()
            elif type_to_verify == 'both' and not self.ftp.exists(self.argv[1]):
                warning("Invalid file: " + self.ftp.sabspath(self.argv[1]))
                return True
            elif type_to_verify == 'dir' and not self.ftp.is_dir(self.argv[1]):
                warning("Invalid file: " + self.ftp.sabspath(self.argv[1]))
                return True
            elif type_to_verify == 'file' and not self.ftp.is_file(self.argv[1]):
                warning("Invalid file: " + self.ftp.sabspath(self.argv[1]))
                return True
            else:
                funtion_2_args()
                return False
        elif self.argc == 3:
            if type_to_verify == 'both' and not self.ftp.exists(self.argv[2]):
                warning("Invalid file or directory: " + self.ftp.sabspath(self.argv[2]))
                return True
            elif type_to_verify == 'dir' and not self.ftp.is_dir(self.argv[2]):
                warning("Invalid directory: " + self.ftp.sabspath(self.argv[2]))
                return True
            elif type_to_verify == 'file' and not self.ftp.is_file(self.argv[2]):
                warning("Invalid file: " + self.ftp.sabspath(self.argv[2]))
                return True
            elif self.argv[1][0] == "-":
                funtion_3_args()
                return False
            else:
                error("usage : {} [OPTION] <path>".format(self.argv[0]))
                return True
        elif self.argc > 3:
            error("usage : {} [OPTION] <path>".format(self.argv[0]))
            return True
        else:
            return False
