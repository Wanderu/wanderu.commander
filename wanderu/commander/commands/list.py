######################
# Description:
# List all commands.
#
# Author: Melih Elibol
# Email: elibol@wanderu.com
# Copyright Wanderu, 2014
######################


from wanderu.commander.commanddescription import description
from wanderu.commander import modutils
from wanderu.commander.commandbase import CommandBase

@description("Lists all commands.")
class List(CommandBase):

    def __init__(self, *args, **kwargs):
        """
        mod_path: List of module path segments.
                  IE. for module 'wgraph.commands' this would be
                      ["wgraph", "commands"]
        """
        self.mod_path = kwargs.pop("mod_path", None)
        super(List, self).__init__(*args, **kwargs)

    def execute(self, **kwargs):
        _code = super(List, self).execute(**kwargs)
        if _code > 0:
            return _code
        print "\nCommands:"
        self.print_commands(self.mod_path, [], 0)
        return 0

    def print_commands(self, mod_path, parents, level):
        if level > 10:
            print "Potential infinite loop detected. Exiting."
            return
        cmds = modutils.get_package_modules(mod_path)
        for cmd in cmds:
            # print mod_path, cmd
            cmd_cls = modutils.get_command_cls(*(mod_path+[cmd]))
            if cmd_cls is None:
                self.print_commands(mod_path+[cmd], parents+[cmd], level+1)
            else:
                if len(parents) == 0:
                    print cmd.lower()
                else:
                    print " ".join(parents), cmd.lower()

                    """
                    try:
                        print "- ", cmd_cls().describe().description
                    except Exception as e:
                        pass
                    """

    def get_commands(self):
        return self._get_commands(self.mod_path, [], 0, [])

    def _get_commands(self, mod_path, parents, level, result):
        if level > 10:
            print "Potential infinite loop detected. Exiting."
            return None
        cmds = modutils.get_package_modules(mod_path)
        for cmd in cmds:
            # print mod_path, cmd
            cmd_cls = modutils.get_command_cls(*(mod_path+[cmd]))
            if cmd_cls is None:
                # TODO: raise exception if cmd_cls is actually a class
                result = self._get_commands(mod_path+[cmd],
                                            parents+[cmd],
                                            level+1,
                                            result)
            else:
                if len(parents) == 0:
                    result.append({"name": cmd.lower(), "class": cmd_cls})
                else:
                    result.append({"name": " ".join(parents)+" "+cmd.lower(),
                                   "class": cmd_cls})
        return result
