#coding:utf-8

class ls:
    def __init__(self, args, ftp, address = "127.0.0.1", user = ""):
        self.args = args
        self.ftp = ftp
        self.address = address
        self.user = user

    def call(self):
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
