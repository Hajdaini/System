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

    def input_error_handle(self, args):
        errors = []
        for el in args:
            if "callback" not in el:
                warning("Callnack function must be given")
            files = el["files"] if "files" in el else "reject"
            options = el["options"] if "options" in el else "reject"
            hasoption = self.argc >= 2 and len(self.argv[1]) and self.argv[1][0] == "-"
            if "nargs" in el and files not in "reject":
                if el["nargs"] == "" or ":" in el["nargs"]:
                    nargs = el["nargs"].split(":")
                else:
                    nargs = [el["nargs"], el["nargs"]]
                nargc = self.argc - 2 if hasoption else self.argc - 1
                if nargs[0] != "" and int(nargs[0]) and files in "accept":
                    nargs[0] = ""
                if len(nargs) == 1 or len(nargs) >= 3:
                    nargs = ["1", ""] if files in "require" else ["0", ""]
                if nargs[0] == "0" and files in "require":
                    nargs[0] = "1"
                if nargs[0] == "" and nargc > int(nargs[1]):
                    errors.append("Invalid number of arguments")
                    continue
                elif nargs[1] == "" and nargc < int(nargs[0]):
                    errors.append("Invalid number of arguments")
                    continue
                elif nargs[0] != "" and nargs[1] != "" and (nargc < int(nargs[0]) or nargc > int(nargs[1])):
                    errors.append("Invalid number of arguments")
                    continue
            if files in "require":
                if self.argc == 2:
                    if hasoption:
                        if options not in "reject":
                            errors.append("Command requires almost one filename")
                            continue
                        else:
                            errors.append("Command accepts only files")
                            continue
                    elif not hasoption and options in "require":
                        errors.append("Command requires options")
                        continue
                    else:
                        el["callback"]()
                        continue
            elif files in "reject":
                if self.argc >= 3:
                    errors.append("Command do not accept filenames")
                    continue
                elif self.argc == 2 and not hasoption:
                    errors.append("Command do not accept filenames")
                    continue
            if options in "require" and (self.argc == 1 or not hasoption):
                errors.append("Command options are required")
                continue
            elif options in "reject" and (self.argc == 1 or hasoption):
                errors.append("Command do not accept options")
                continue
            else:
                el["callback"]()
                continue
        if len(errors) == len(args):
            warning(errors[0])
    """

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
    """
