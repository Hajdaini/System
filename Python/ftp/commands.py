#coding:utf-8

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

def cd(args, ftp, address, user):
    try:
        ftp.sendcmd('CWD {}'.format(args[1]))
    except:
        print('Directory may not exist or you may not have permission to view it.')
    return ftp

def ls(args, ftp, address, user):
    if len(args) == 1:
        ftp.dir()
    elif len(commands) == 2:
        ftp.dir(args[1])
    else:
        print("Error (Usage : ls <path>)")
    return ftp

def cat(args, ftp, address, user):
    try:
        file = "{}/{}".format(ftp.pwd(), args[1])
        with open(file, "r") as file:
            print(file.read())
    except :
        print('File may not exist or you may not have permission to access it.')
    return ftp

def get(args, ftp, address, user):
    try:
        file = "{}/{}".format(ftp.pwd(), args[1])
        print("Downloading ...")
        if is_dir(ftp, file):
            download_tree(ftp, file)
        else:
            ftp.retrbinary('RETR ' + args[1], open(args[1], 'wb').write)
        print('Download success !')
    except :
        print('File may not exist or you may not have permission to view it.')
    return ftp

def put(args, ftp, address, user):
    try:
        file = "{}/{}".format(ftp.pwd(), args[1])
        Oftp.storbinary('STR {}'.format(args[1]), open(file, 'rb'))
    except :
        print("You may not have permission to upload")
    return ftp

def mkdir(args, ftp, address, user):
    try:
        file = "{}/{}".format(ftp.pwd(), args[1])
        print(file)
        ftp.mkd(file)
    except :
        print("You may not have permission to create folder")
    return ftp

def rm(args, ftp, address, user):
    try:
        file1 = "{}/{}".format(ftp.pwd(), args[1])
        file2 = "{}/{}".format(ftp.pwd(), args[2])
        if args[1] == '-d' or args[1] == '-D':
            ftp.rmd(file2)
        else:
            ftp.delete(file1)
    except :
        print("You may not have permission to delete file or folder")
    return ftp

def help(args, ftp, address, user):
    print(help_content)
    return ftp

def exit(args, ftp, address, user):
    ftp.quit()
    print('Goodbye!')
    return ftp
