#coding:utf-8

help_content = """
- help : see the possible commands
- ls [path] : lists the contents of, and optional information about, directories and files
- cat [path] : read data from files
- get [path] : download a file or directory (recursively) from ftp to local
- cd <path> : change the directory
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
        with open("{}/{}".format(ftp.pwd(), args[1]), "r") as file:
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

def help(args, ftp, address, user):
    print(help_content)
    return ftp

def exit(args, ftp, address, user):
    ftp.quit()
    print('Goodbye!')
    return ftp
