from cx_Freeze import setup, Executable

setup(
    name = "ftp",
    version = "0.0.1",
    description = "Script de gestion FTP",
    executables = [Executable("Python/main.py")]
)
