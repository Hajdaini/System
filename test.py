import ftplib
import os
import re
from getpass import getpass


help_content = """
- help : see the possible commands
- ls [path] : lists the contents of, and optional information about, directories and files
- cat [path] : read data from files
- get [path] : download a file or directory (recursively) from ftp to local
- cd <path> : change the directory
- exit : exit the script
"""


def connect(address, user, password, port):
    while True:
        try:
            ftp = ftplib.FTP(address, user, password)
            ftp.connect(address, int(port))
            return ("connected", ftp)
        except ftplib.all_errors as e:
            return ("failed", e)


def is_ftp_dir(ftp_handle, name):
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


def download_ftp_file(ftp_handle, name, dest, overwrite):
    create_parent_dir(dest.lstrip("/"))
    if not os.path.exists(dest) or overwrite is True:
        try:
            with open(dest, 'wb') as f:
                ftp_handle.retrbinary("RETR {0}".format(name), f.write)
            print("downloaded: {0}".format(dest))
        except FileNotFoundError:
            print("FAILED: {0}".format(dest))
    else:
        print("already exists: {0}".format(dest))


def mirror_ftp_dir(ftp_handle, name, overwrite):
    for item in ftp_handle.nlst(name):
        if is_ftp_dir(ftp_handle, item): # if it is a directory then we don't care
            mirror_ftp_dir(ftp_handle, item, overwrite)
        else:
            download_ftp_file(ftp_handle, item, item, overwrite)


def download_ftp_tree(ftp_handle, path, overwrite=False):
    path = path.lstrip("/")
    original_directory = os.getcwd()
    mirror_ftp_dir(ftp_handle, path, overwrite)
    os.chdir(original_directory)


def ftp_command(ftp, user, address):
    while True:
        command = input("ftp://{}@{}:{} > ".format(user, address, ftp.pwd()))
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

# Donnees de connexion par defaut
state = "idle"
address = "127.0.0.1"
user = ""
password = ""
port="21"
tmp = ""

# connecteur
while state != "connected":
    if state == "error":
        print("\nFTP failed to connect: {}".format(res))

    tmp = input("FTP Host ({}): ".format(address))
    address = tmp if tmp != "" else address

    tmp = input("FTP User ({}): ".format(user))
    user = tmp if tmp != "" else user

    tmp = getpass("FTP Password: ")
    password = tmp if tmp != "" else password

    tmp = input("FTP Port ({}): ".format(port))
    port = tmp if tmp != "" else port

    state, res = connect(address, user, password, port)

ftp_command(res, user, address)
