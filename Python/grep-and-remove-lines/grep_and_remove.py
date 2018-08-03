"""
@Author : AJDAINI Hatim
@GitHub : https://github.com/Hajdaini
"""

import sys

if len(sys.argv) != 3:
    print('Il manque des arguments, il faut utiliser le script comme ceci :')
    print('python3 grep_and_remove.py chemin_du_fichier mot_a_verifier')
else:
    path = sys.argv[1]
    word = sys.argv[2]

    lines = []

    with open(path, 'r') as file:
        lines = file.readlines()

    with open(path, 'w') as file:
        for line in lines:
            if word not in line:
                file.write(line)
