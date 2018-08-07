import os
from cx_Freeze import setup, Executable

dir_path = os.path.dirname(os.path.realpath(__file__))

setup(
    name = "ftp",
    version = "0.0.1",
    description = "Script de gestion FTP",
    executables = [Executable("{}/main.py".format(dir_path))]
)
