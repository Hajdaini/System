# coding:utf-8

import json
import os.path


class Config:
    config_file_path = os.path.dirname(__file__) + '/../config/ftp.cfg'
    default_data = {
        'address': '127.0.0.1',
        'user': 'anonymous',
        'port': 21,
        'timeout': 600
    }

    @classmethod
    def load(cls):
        with open(cls.config_file_path, 'r') as data_file:
            data = json.load(data_file)
        return data

    @classmethod
    def save(cls, data):
        with open(cls.config_file_path, 'w') as outfile:
            json.dump(data, outfile, indent=4, separators=(',', ': '))

    @classmethod
    def save_default(cls):
        with open(cls.config_file_path, 'w') as outfile:
            json.dump(cls.default_data, outfile, indent=4, separators=(',', ': '))
