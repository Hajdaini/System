# coding:utf-8

import json
import os.path
from modules.color import cprint


class Config:
    config_file_path = os.path.dirname(os.path.dirname(__file__)) + '/config/ftp.cfg'

    @classmethod
    def load(cls, file="ftp"):
        path = cls.config_file_path.replace("ftp.cfg", file) + ".cfg"
        with open(path, 'r') as data_file:
            data = json.load(data_file)
        return data

    @classmethod
    def save(cls, data, file="ftp"):
        path = cls.config_file_path.replace("ftp.cfg", file) + ".cfg"
        with open(path, 'w') as outfile:
            json.dump(data, outfile, indent=4, separators=(',', ': '))

    @classmethod
    def save_default(cls, file="ftp"):
        srcpath = cls.config_file_path.replace("ftp.cfg", "RECOVERY_CONFIG/" + file) + ".cfg.old"
        destpath = cls.config_file_path.replace("ftp.cfg", file) + ".cfg"
        with open(srcpath, "r") as srcfile:
            default_data = json.load(srcfile)
            with open(destpath, 'w') as destfile:
                json.dump(default_data, destfile, indent=4, separators=(',', ': '))

    @classmethod
    def get_config_path_for_print_only(cls, file="ftp"):
        path = os.path.dirname(os.path.dirname(__file__)) + ('/config/[b]' + file + '.cfg[/b]')
        if os.name == 'nt':
            path = path.replace('/', '\\')
        return path

    @classmethod
    def display_config(cls, file="ftp", show=[], hide=[], prefix_filename=True, keep_show_order=True):
        cprint(file.upper() + " config file: [warning]{}[/warning]".format(cls.get_config_path_for_print_only(file)))
        data = cls.load()
        if keep_show_order and len(show):
            for k in show:
                if k in data and not k in hide:
                    output = "{}: [green]{}[/green]"
                    if prefix_filename:
                        output = "{} {}".format(file.upper(), output)
                    cprint(output.format(k.capitalize(), data[k]))
        else:
            for k, v in data.iteritems():
                if (k in show or not len(show)) and k not in hide:
                    output = "{}: [green]{}[/green]"
                    if prefix_filename:
                        output = "{} {}".format(file.upper(), output)
                    cprint(output.format(k.capitalize(), v))

    @classmethod
    def is_ftps(cls):
        data = cls.load()
        return data['ftps']

    @classmethod
    def is_prot_d(cls):
        data = cls.load()
        return data["ftps"] and data['prot_d']
