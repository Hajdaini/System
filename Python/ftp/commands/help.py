#coding:utf-8

import importlib
import pkgutil
import commands
from modules.Command import Command
from modules.color import warning, color

class help(Command):
    """
    [b]NAME:[/b] help

    Get help about any available Command

    [b]SYNOPSIS:[/b]

    [b]help[/b]
    [b]help[/b] <[u]command[/u]>

    [b]DESCRIPTION:[/b]

    Called without argument, help gives a list of all available commands
    If a command is specified, help displays the specific command documentation
    """
    def __init__(self, args, ftp, address, user):
        Command.__init__(self, args, ftp, address, user)

    def call(self):
        if self.argc == 2:
            try:
                cmd = importlib.import_module("commands.{}".format(self.argv[1]))
                cls = getattr(cmd, self.argv[1])
                if cls.__doc__ == None:
                    warning("Unavailable documentation")
                else:
                    color(cls.__doc__, True)
            except:
                warning("Command {} not found. Type help to get available commands".format(self.argv[1]))
        elif self.argc == 1:
            print("Usage:")
            color("\t[b]help[/b] : get list of all commands", True)
            color("\t[b]help <[u]commandName[/u][b]>[/b] : get a specific command documentation", True)
            print("Available commands:")
            package = commands
            for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
                if modname[0].islower():
                    color("\t[b]{}[/b]".format(modname), True)
        else:
            warning("Bad usage of help command")
