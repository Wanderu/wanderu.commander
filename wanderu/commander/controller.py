######################
# Description:
# Simple controller that invokes commands.
######################

from itertools import chain
from types import StringTypes
from wanderu.commander import modutils

class Controller(object):

    def __init__(self, pkg):
        """
        pkg: The name of the package under which commands are placed.
             IE. mypackage.mymod.commands
             Or, a list/tuple represending the package that contains the
             commands.
             IE. ['mypackage', 'mymod', 'commands']
        """
        if isinstance(pkg, StringTypes):
            self.pkg = pkg.split(".")
        else:
            self.pkg = pkg

    def __getattr__(self, name):
        command_cls = modutils.get_command_cls(*chain(self.pkg, (name,)))
        if command_cls is not None:
            def exec_command(*args):
                return command_cls().execute(*args)
            return exec_command
        else:
            print "No such command."
            return lambda: []

    def find_command(self, *args):
        mod_path = self.pkg[:]
        args = list(args)
        #print args
        command_mod = []
        while len(args) > 0:
            i = args.pop(0)
            mod_path.append(i)
            command_mod.append(i)
            #print mod_path
            command_cls = modutils.get_command_cls(*mod_path)
            if command_cls is not None:
                return command_cls, command_mod, args
        return None, [], []
