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

def cat(args, ftp, address, user):
    try:
        with open(args[1], "r") as file:
            print(file.read())
    except :
        print('File may not exist or you may not have permission to access it.')

def get(args, ftp, address, user):
    try:
        print("Downloading ...")
        if is_ftp_dir(ftp, args[1]):
            download_ftp_tree(ftp, commands[1])
        else:
            ftp.retrbinary('RETR ' + commands[1], open(commands[1], 'wb').write)
        print('Download success !')
    except :
        print('File may not exist or you may not have permission to view it.')

def help(args, ftp, address, user):
    print(help_content)

def exit(args, ftp, address, user):
    ftp.quit()
    print('Goodbye!')