#coding:utf-8

from ftplib import FTP
from modules.Capture import Capture
import sys
import os

ftp = FTP("127.0.0.1")
ftp.login(user=sys.argv[1], passwd=sys.argv[2])
home = ftp.pwd()

def cabspath(pwd, path):
    if path[0] == "/":
        return path
    pwd = pwd.split("/")
    del pwd[0]
    cpath = path.split("/")
    for idx, el in enumerate(path.split("/")):
        if el == ".." or el == ".":
            del cpath[0]
            if el == ".." and len(pwd):
                pwd.pop()
        else:
            break
    if (len(pwd)):
        pwd[0] = "/{}".format(pwd[0])
    return "{}/{}".format("/".join(pwd), "/".join(cpath))

def labspath(path):
    pwd = os.path.dirname(os.path.abspath(__file__))
    return cabspath(pwd, path)

def sabspath(ftp, path):
    pwd = ftp.pwd()
    return cabspath(pwd, path)

def ls_info(ftp, path):
    path = sabspath(ftp, path)
    info = {}
    with Capture() as output:
        ftp.dir(path)
    if output == "":
        return {}
    for line in output:
        line = line.split()
        file = line[len(line) - 1]
        isdir = line[0][0] == "d"
        line[0] = line[0][1:]
        info[file] = {
            "type": "dir" if isdir else "file",
            "chmod": line[0],
            "hardlinks" : line[1],
            "size" : line[4],
            "modified": " ".join(line[5:-1]),
            "name": file
        }
    return info

def is_empty(ftp, path):
    path = sabspath(ftp, path)
    if not exists(ftp, path) or is_file(ftp, path):
        return False
    with Capture() as output:
        ftp.dir(path)
    return len(output) == 0

def is_dir(ftp, path="./"):
    path = sabspath(ftp, path)
    if len(path) == 1 and path[0] == "/":
        return True
    test = path.split("/")
    test = test[len(test) - 1]
    path = cabspath(path, "../")
    ls = ls_info(ftp, path)
    return test in ls and ls[test]["type"] == "dir"

def is_file(ftp, path):
    path = sabspath(ftp, path)
    if len(path) == 1 and path[0] == "/":
        return False
    test = path.split("/")
    test = test[len(test) - 1]
    path = cabspath(path, "../")
    ls = ls_info(ftp, path)
    return test in ls and ls[test]["type"] == "file"

def exists(ftp, path):
    path = sabspath(ftp, path)
    if len(path) == 1 and path[0] == "/":
        return False
    test = path.split("/")
    test = test[len(test) - 1]
    path = cabspath(path, "../")
    ls = ls_info(ftp, path)
    return test in ls

def cat_file(ftp, srcpath):
    srcpath = sabspath(ftp, srcpath)
    ftp.retrlines("RETR " + srcpath, print)

def grab_file(ftp, srcpath, destpath=None):
    if destpath == None:
        destpath = srcpath
    srcpath = sabspath(ftp, srcpath)
    destpath = labspath(destpath)
    destfile = open(destpath, "wb")
    ftp.retrbinary("RETR " + srcpath, destfile.write)
    destfile.close()

def place_file(ftp, srcpath, destpath=None):
    if destpath == None:
        destpath = srcpath
    srcpath = labspath(srcpath)
    destpath = sabspath(ftp, destpath)
    srcfile = open(srcpath, "rb")
    ftp.storbinary("STOR " + destpath, srcfile)
    srcfile.close()

def ls_path(ftp, cmd):
    if len(cmd) == 3 and cmd[1] == "-l" and exists(ftp, cmd[2]):
        ftp.dir(sabspath(ftp, cmd[2]))
    elif len(cmd) == 2 and cmd[1] != "-l" and exists(ftp, cmd[1]):
        print(" ".join(ftp.nlst(sabspath(ftp, cmd[1]))))
    elif len(cmd) == 2 and cmd[1] == "-l":
        ftp.dir()
    elif len(cmd) == 1:
        print(" ".join(ftp.nlst()))
    else:
        print("Invalid path")

def rm_path(ftp, path):
    if len(cmd) == 3 and (cmd[1] == "-d" or cmd[1] == "-D") and is_dir(cmd[2]):
        ftp.rmd(sabspath(cmd[2]))
    elif len(cmd) == 2 and is_file(cmd[1]):
        ftp.delete(sabspath(cmd[1]))
    else:
        print("File not exists or permission denied")

def cd_path(ftp, cmd):
    if len(cmd) == 2 and is_dir(ftp, cmd[1]):
        ftp.cwd(sabspath(ftp, cmd[1]))
    elif len(cmd) == 1:
        ftp.cwd(home)

def mkdir(ftp, cmd):
    if not exists(cmd[1]):
        ftp.mkd(sabspath(cmd[1]))
    else:
        print("file alor directory ready exists")

def sizeof(ftp, cmd):
    if exists(cmd[1]):
        ftp.size(sabspath(ftp, cmd[1]))
    else:
        print("invalid path")

def mv(ftp, from, to):
    from = sabspath(from)
    to = sabspath(to)
    if exists(from) and not exists(to):
        ftp.rename(from, to)

def cp(ftp, from, to):
    from = sabspath(from)
    to = sabspath(to)
    if is_file(from) and not exists(to):
        pass

while True:
    cmd = input("{}$>".format(ftp.pwd()))
    if cmd == "":
        continue
    cmd = cmd.split()
    if cmd[0] == "pwd":
        print(ftp.pwd())
    elif cmd[0] == "cd":
        cd_path(ftp, cmd)
    elif cmd[0] == "sizeof":
        sizeof(ftp, cmd)
    elif cmd[0] == "grab":
        grab_file(ftp, cmd[1])
    elif cmd[0] == "place":
        place_file(ftp, cmd[1])
    elif cmd[0] == "cat":
        cat_file(ftp, cmd[1])
    elif cmd[0] == "isdir":
        print(is_dir(ftp, cmd[1]))
    elif cmd[0] == "isfile":
        print(is_file(ftp, cmd[1]))
    elif cmd[0] == "exists":
        print(exists(ftp, cmd[1]))
    elif cmd[0] == "isempty":
        print(is_empty(ftp, cmd[1]))
    elif cmd[0] == "info":
        ls_info(ftp, cmd[1])
    elif cmd[0] == "ls":
        ls_path(ftp, cmd)
    elif cmd[0] == "rm":
        rm_path(ftp, cmd)
    elif cmd[0] == "mkdir":
        mkdir(ftp, cmd)
    elif cmd[0] == "mv":
        mv(ftp, cmd[1], cmd[2])
    elif cmd[0] == "exit":
        print("Good Bye!")
        sys.exit(1)
    else:
        print("Command not found")
