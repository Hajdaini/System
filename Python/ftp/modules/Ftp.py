#coding:utf-8

from ftplib import FTP

class Ftp(FTP):
    def __init__(self, host="127.0.0.1", timeout=30):
        FTP.__init__(self, host, timeout=timeout)

    def is_dir(self, name):
        r1 = re.findall(r"type=(file|dir)", self.sendcmd('MLST {}'.format(name)))
        type = ''.join(r1)
        return type == "dir"

    def create_parent_dir(self, fpath):
        dirname = os.path.dirname(fpath)
        while not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
                print("created directory : {0}".format(dirname))
            except:
                create_parent_dir(dirname)

    def download_file(self, name, dest, overwrite):
        self.create_parent_dir(dest.lstrip("/"))
        if not os.path.exists(dest) or overwrite is True:
            try:
                with open(dest, 'wb') as f:
                    self.retrbinary("RETR {0}".format(name), f.write)
                print("Downloaded: {0}".format(dest))
            except FileNotFoundError:
                print("FAILED: {0}".format(dest))
        else:
            print("Already exists: {0}".format(dest))

    def download_tree(self, path, overwrite=False):
        path = path.lstrip("/")
        original_directory = os.getcwd()
        self.mirror_dir(path, overwrite)
        os.chdir(original_directory)

    def mirror_dir(self, name, overwrite):
        for item in self.nlst(name):
            if self.is_dir(item): # if it is a directory then we don't care
                self.mirror_dir(item, overwrite)
            else:
                self.download_file(item, item, overwrite)
