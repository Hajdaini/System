#coding:utf-8

from pathlib import Path
import pickle

def read(path="./", mode="r"):
    if not Path().is_file(path):
        return None
    try:
        with open(path, mode) as file:
            return file.read()
    except:
        return None

def write(path="./", data=None,  mode="w"):
    if not Path().is_file(path):
        return False
    try:
        with open(path, mode) as file:
            file.write(str(data))
            return True
    except:
        return False

def readbin(path="./", mode="r"):
    if not Path().is_file(path):
        return None
    try:
        with open(path, mode + "b") as file:
            record = pickle.Unpickler(file)
            return record.load()
    except:
        return None

def writebin(path="./", data=None,  mode="w"):
    if not Path().is_file(path):
        return False
    try:
        with open(path, mode + "b") as file:
            record = pickle.Pickler(file)
            record.dump(data)
            return True
    except:
        return False
