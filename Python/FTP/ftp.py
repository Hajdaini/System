#coding:utf-8

import ftplib
import os
import re
from FTP import commands


<<<<<<< HEAD
def connect(address="127.0.0.1", user="", password="", port="21"):
=======
help_content = """
- help : see the possible commands
- ls [path] : lists the contents of, and optional information about, directories and files
- cat [path] : read data from files
- get [path] : download a file or directory (recursively) from ftp to local
- cd <path> : change the directory
- put <file> : upload file in the ftp server
- rm [-d] path : remove a file from ftp server (-d to remove directories)
- mkdir <folder> : create a folder in the ftp server
- exit : exit the script
"""


def ftp_connect():
    while True:
        user = input('Please enter FTP user: ')
        password = input('Please enter FTP password: ')
        address = input('Please enter FTP address: ')
>>>>>>> 8b8b58ea23779799790d602e9615a8ab02a43fa7
        try:
            ftp = ftplib.FTP(address, user, password)
            # ftp.connect(address, int(port))
            return ("connected", ftp)
        except ftplib.all_errors as e:
            return ("failed", e)


def is_dir(ftp_handle, name):
    r1 = re.findall(r"type=(file|dir)", ftp_handle.sendcmd('MLST {}'.format(name)))
    type = ''.join(r1)
    return type == "dir"


def create_parent_dir(fpath):
    dirname = os.path.dirname(fpath)
    while not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
            print("created directory : {0}".format(dirname))
        except:
            create_parent_dir(dirname)


def download_file(ftp_handle, name, dest, overwrite):
    create_parent_dir(dest.lstrip("/"))
    if not os.path.exists(dest) or overwrite is True:
        try:
            with open(dest, 'wb') as f:
                ftp_handle.retrbinary("RETR {0}".format(name), f.write)
            print("Downloaded: {0}".format(dest))
        except FileNotFoundError:
            print("FAILED: {0}".format(dest))
    else:
        print("Already exists: {0}".format(dest))


def mirror_dir(ftp_handle, name, overwrite):
    for item in ftp_handle.nlst(name):
        if is_ftp_dir(ftp_handle, item): # if it is a directory then we don't care
            mirror_ftp_dir(ftp_handle, item, overwrite)
        else:
            download_ftp_file(ftp_handle, item, item, overwrite)


def download_tree(ftp_handle, path, overwrite=False):
    path = path.lstrip("/")
    original_directory = os.getcwd()
    mirror_ftp_dir(ftp_handle, path, overwrite)
    os.chdir(original_directory)


def interpreter(ftp, address="", user=""):
    while True:
        command = input("ftp://{}@{}:{} > ".format(user, address, ftp.pwd()))
<<<<<<< HEAD
        command = command.split()
=======
        commands = command.split()

        if commands[0] == 'cd':
            try:
                ftp.sendcmd('CWD {}'.format(commands[1]))
            except:
                print('Directory may not exist or you may not have permission to view it.')
        elif commands[0] == 'cat':
            try:
               with open(commands[1], "r") as file:
                   print(file.read())
            except :
                print('File may not exist or you may not have permission to view it.')
        elif commands[0] == 'get':
            try:
                print("Downloading ...")
                if is_ftp_dir(ftp, commands[1]):
                    download_ftp_tree(ftp, commands[1])
                else:
                    ftp.retrbinary('RETR ' + commands[1], open(commands[1], 'wb').write)
                print('Download success !')
            except :
                print('File may not exist or you may not have permission to view it.')
        elif commands[0] == 'put':
            try:
                ftp.storbinary('STOR {}'.format(commands[1]), open(commands[1], 'rb'))
            except :
                print("You may not have permission to upload")
        elif commands[0] == 'mkdir':
            try:
                ftp.mkd(commands[1])
            except :
                print("You may not have permission to create folder")
        elif commands[0] == 'rm':
            try:
                if commands[1] == '-d' or commands[1] == '-D':
                    ftp.rmd(commands[2])
                else:
                    ftp.delete(commands[1])
            except :
                print("You may not have permission to delete file or folder")
        elif commands[0] == 'ls':
            if len(commands) == 1:
                ftp.dir()
            elif len(commands) == 2:
                ftp.dir(commands[1])
            else:
                print("Error (Usage : ls <path>)")
        elif commands[0] == 'help':
            print(help_content)
        elif commands[0] == 'exit':
            ftp.quit()
            print('Goodbye!')
            break
        else:
            print('Enter help to see the different commands')
>>>>>>> 8b8b58ea23779799790d602e9615a8ab02a43fa7

        try:
           call = getattr(commands, command[0])
           ftp = call(command, ftp, address, user)
        except:
            print('Enter help to see the different commands')
        if command[0] == "exit":
            break
