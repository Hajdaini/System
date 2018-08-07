NAME=Build # Nom du dossier contenant le build genere par cx_Freeze
SRCD=./Python/ # Chemin vers l'ensemble du code python
SRCF=main.py # Fichier principal du programme

# Ne rien toucher en dessous

all:
	@ echo "Go lire le README!"

run:
	@ echo "Lancement du programme"
	@ python3 ./Python/$(SRCF)

build: freeze

freeze:
	@ python3 ./Python/freeze.py build
	@ echo "Creation du repertoire $(NAME)"
	@mv build $(NAME)

setup: setup_vsftpd setup_pip setup_cxfreeze
	@ echo "Dependances installees"

setup_vsftpd:
	@ echo "Installation du serveur FTP: vsftpd"
	@ sudo apt-get install vsftpd

setup_pip:
	@ echo "Installation de python3-pip"
	@ sudo apt-get install python3-pip

setup_cxfreeze:
	@ echo "Installation de CX_Freeze"
	@ python3 -m pip install cx_Freeze

clean:
	@ echo "Suppression du repertoire $(NAME)"
	@ /bin/rm -rf $(NAME)
