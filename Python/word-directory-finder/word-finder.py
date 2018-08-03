"""
@Author : AJDAINI Hatim
@GitHub : https://github.com/Hajdaini
"""

import os, time, sys, argparse
from argparse import RawTextHelpFormatter

description = """This program find all the files in a folder (recursively) containing the searched word according to a given extension.\n
EXAMPLES :
1) Example with all extension : python -p your_path -w your_word
2) Example with single extension : python -p your_path -w your_word -e txt
3) Example with single extension : python -p your_path -w your_word -e "txt, php\"
3) Example with deepsearch : python -p your_path -w your_word -e "txt, php\" -d"""

parser = argparse.ArgumentParser(description=description, formatter_class=RawTextHelpFormatter)
parser.add_argument("-p", help="[REQUIRED] search directory path")
parser.add_argument("-w", help="[REQUIRED] word to find")
parser.add_argument("-e", help="[OPTIONAL] extensions (if empty or equal to * then it will search for all extensions)", nargs='?')
parser.add_argument("-d", help="""[OPTIONAL] find the word in a word for example if your search word is "cat" it will find also the word that contain "cat" like the word "catalyst" if not enabled if you will ignore it.""", action="store_true")
args = parser.parse_args()

path_arg = args.p
word_arg = args.w
extensions = []
deepSearch = args.d

if args.e == None:
    extensions.append("")
else:
    extensions = args.e.split(" ")

paths = []
paths_erros = []
time_start = time.time()


def get_all_files_and_directories():
    global paths
    global extensions
    if extensions[0] == '*' or not extensions[0]:
        try:
            for root, dirs, files in os.walk(path_arg):
                for file in files:
                    sys.stdout.write('\r' + os.path.join(root, file))
                    paths.append(os.path.join(root, file))
        except:
            quit(0)
    else:
        for root, dirs, files in os.walk(path_arg):
            for file in files:
                sys.stdout.write('\r' + os.path.join(root, file))
                for ext in extensions:
                    if file.endswith('.{}'.format(ext)):
                        paths.append(os.path.join(root, file))


def find_word():
    global paths_erros
    for path in paths:
        try:
            with open(path, 'r', encoding="ISO-8859-1") as file:
                lines = file.read().splitlines()
                for num, line in enumerate(lines, 1):
                    if not deepSearch:
                        line = line.split(" ")
                    if word_arg in line:
                        print('found at line {} in the path "{}"'.format(num, path))
        except:
            paths_erros.append(path)


def check_errors():
    if len(paths_erros) > 0:
        print("\nthe program can not read some files, open the file errors.txt to see them.")
        print("The problem might be because you do not have read permission on the file or the file is corrupted.")
        with open('erros.txt', 'w') as file:
            for path_e in paths_erros:
                file.write("""Can't read the file "{}"\n""".format(path_e))


if __name__ == '__main__':
    get_all_files_and_directories()
    load_done = True

    print('\n\nResult :')
    find_word()
    check_errors()
    print('Finish in {} s'.format(round(time.time() - time_start, 3)))
