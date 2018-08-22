# coding:utf-8

import json
import os.path
from modules.color import cprint


class Config:
    config_file_path = os.path.dirname(os.path.dirname(__file__)) + '/config/ftp.cfg'
    default_data = {
        'ftps': True,
        'prot_d': True,
        'address': '127.0.0.1',
        'user': 'anonymous',
        'port': 21,
        'timeout': 600
    }

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
    def save_default(cls):
        with open(cls.config_file_path, 'w') as outfile:
            json.dump(cls.default_data, outfile, indent=4, separators=(',', ': '))

    @classmethod
    def get_config_path_for_print_only(cls):
        return os.path.dirname(os.path.dirname(__file__)) + ('\config\[b]ftp.cfg[/b]' if os.name == 'nt' else '/config/[b]ftp.cfg[/b]')

    @classmethod
    def display_config(cls):
        cprint("FTP config file: [warning]{}[/warning]".format(cls.get_config_path_for_print_only()))
        data = cls.load()
        cprint("FTP User: [green]{}[/green]".format(data['user']))
        cprint("FTP Address: [green]{}[/green]".format(data['address']))
        cprint("FTP Port: [green]{}[/green]".format(data['port']))
        cprint("FTP Timeout: [green]{}[/green]".format(data['timeout']))

    @classmethod
    def is_ftps(cls):
        data = cls.load()
        return data['ftps']

    @classmethod
    def is_prot_d(cls):
        data = cls.load()
        return data["ftps"] and data['prot_d']
