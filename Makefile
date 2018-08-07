NAME=ftp
SRCD=./Python/
SRCS=main

all:
	@ echo "Go lire le README!"

run:
	@ python3 ./Python/main.py

freeze:
	@ python3 ./Python/freeze.py build
	@mv build Build

setup: setup_vsftpd setup_cxfreeze

setup_vsftpd:
	@ echo "Installation du serveur FTP: vsftpd"
	@ sudo apt-get install vsftpd

setup_cxfreeze:
	@ echo "Installation de CX_Freeze\n"
	@ python3 -m pip install cx_Freeze
