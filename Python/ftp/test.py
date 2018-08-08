import pkgutil

# this is the package we are inspecting -- for example 'email' from stdlib
import commands

package = commands
for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
    print("Found submodule {} (is a package: {})".format(modname, ispkg))
