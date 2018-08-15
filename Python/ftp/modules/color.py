# coding: utf-8

import sys


def color(str, display=False):
    old = [
        "endc",
        "header",
        "blue",
        "green",
        "warning",
        "fail",
        "b",
        "u"
    ]
    new = [
        '\033[0m',
        '\033[95m',
        '\033[94m',
        '\033[92m',
        '\033[93m',
        '\033[91m',
        '\033[1m',
        '\033[4m'
    ]
    for idx, el in enumerate(new):
        str = str.replace("[{}]".format(old[idx]), el)
        str = str.replace("[/{}]".format(old[idx]), new[0])
    if display != True:
        return str
    else:
        print(str)


def cprint(text):
    color(text, True)


def cinput(str):
    return input(color(str))


def info(str):
    color("[blue][b][INFO][/endc] [blue]{}[/blue]".format(str), True)


def success(str):
    color("[green][b][SUCCESS] [green]{}[/green]".format(str), True)


def error(str):
    color("[fail][b][ERROR][/endc] [fail]{}[/fail]".format(str), True)


def fatal(str):
    color("[fail][b][FATAL ERROR][/endc] [fail]{}[/fail]".format(str), True)
    sys.exit(1)


def warning(str):
    color("[warning][b][WARNING][/endc] [warning]{}[/warning]".format(str), True)
