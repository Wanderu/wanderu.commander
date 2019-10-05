######################
# Description:
# Auto-detect commands
# and expose them via argparse.
######################

import sys
import textwrap
import time
from types import NoneType

import argparse

from wanderu.commander.commands.list import List
from wanderu.commander.controller import Controller
from wanderu.commander.commanddescription import ParamAction

# May be of use at some point.
class WanderuHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    def add_usage(self, *args, **kwargs):
        super(WanderuHelpFormatter, self).add_usage(*args, **kwargs)

# TODO: Refactor as CommandBase parameters.
# TODO: Add --examples argument which outputs examples of a command.
def add_general_options(parser):
    # parser.add_argument('-h', '--help', help='show this help message',
    #                     action="store_true", default=False)
    parser.add_argument('--verbose', dest='verbose',
                        action='store_true', default=False,
                        help='Make output verbose.')
    parser.add_argument('-t', '--time', dest='time',
                        action='store_true', default=False,
                        help=('Output the time it took for command to execute, '
                              'in seconds. This may be inaccurate for '
                              'commands that require user input.'))

def basic_parser(prog, desc, version):
    # usage = '%(prog)s <command> [options]'
    parser = argparse.ArgumentParser(description=desc,
                                   version=version,
                                   add_help=True,
                                   formatter_class=WanderuHelpFormatter)

    add_general_options(parser)
    return parser

def print_command_help(parser):
    parser.print_help()

def com_help_str(com):
    desc = ""
    try:
        desc = com['class'].__description
    except:
        pass
    name = "  "+com['name']
    res = "\n"
    col1 = 30
    col2 = 30
    remaining = col1
    res += name
    remaining -= len(name)
    res += textwrap.fill(desc,
                         col1+col2,
                         initial_indent=" "*remaining,
                         subsequent_indent=" "*col1)
    return res

def command_parser(prog, command_mod, command, args, version):
    desc = getattr(command, '__description', '')
    extended_desc = getattr(command, '__extended_desc', '')
    params = getattr(command, '__parameters', [])
    command_name = ' '.join(command_mod)

    parser = argparse.ArgumentParser(description=desc+" "+extended_desc,
                                     prog=prog+" "+command_name,
                                     formatter_class=WanderuHelpFormatter,
                                     version=version,
                                     # usage=usage,
                                     add_help=True)

    add_general_options(parser)
    cmdoptions = parser.add_argument_group("command options")

    for parameter in params:
        action = parameter.action
        if action is ParamAction:
            action = action.value

        isflag = action == ParamAction.STORE_TRUE.value \
                    or action == ParamAction.STORE_FALSE.value

        nameparam = []
        cmdkwargs = {}
        argtarget = cmdoptions
        if not isflag:
            if parameter.ptype is not NoneType:
                cmdkwargs['type'] = parameter.ptype

        if parameter.choices is not None:
            cmdkwargs['choices'] = parameter.choices

        if parameter.optional:
            if parameter.name is not None:
                nameparam.append('--'+parameter.name)
            if parameter.shortname is not None:
                nameparam.append("-"+parameter.shortname)
            # cmdkwargs['dest'] = parameter.name
        else:
            argtarget = parser

        argtarget.add_argument(*nameparam,
                                help=parameter.description,
                                default=parameter.default,
                                action=action,
                                dest=parameter.name,
                                **cmdkwargs)
    return parser

class Commander(object):
    def __init__(self, prog, module, desc, version):
        self.mod_name = module.split(".")
        self.desc     = desc
        self.version  = version
        self.prog     = prog
        self.parser   = basic_parser(prog, desc, version)
        self.lister   = List(mod_path=self.mod_name)

    def print_general_help(self):
        self.parser.print_help()
        print(self.add_command_options(""))

    def add_command_options(self, s):
        s += "\ncommands:"
        comlist = self.lister.get_commands()
        for com in comlist:
            s += com_help_str(com)
        return s

    def execute(self):
        """
        This method returns the exit code of the program.
        """

        starttime = time.time()
        controller = Controller(pkg=self.mod_name)

        prog_args = sys.argv[1:]

        code = 0

        has_help = '--help' in prog_args or '-h' in prog_args
        has_no_args = len(filter(lambda x: x.find("-")==-1, prog_args)) == 0
        if has_no_args:
            self.print_general_help()
            if has_help:
                return 0
            return 1
        else:
            CommandCls = None

            try:
                CommandCls, command_mod, cmd_args = \
                    controller.find_command(*prog_args)
            except ImportError:
                # will be caught by the next section
                pass

            if CommandCls is None:
                # gargs = self.parser.parse_args()
                print("Error: Command not found\n")
                self.print_general_help()
                return 1

            com_parser = command_parser(self.prog,
                                        command_mod,
                                        CommandCls,
                                        cmd_args,
                                        self.version)
            parsed_args = com_parser.parse_args(cmd_args)
            if 'help' in parsed_args and parsed_args.help:
                print_command_help(com_parser)  # used to exit here
                return 0
            code = CommandCls().execute(**vars(parsed_args))
            if parsed_args.time:
                print("\nrunning time: "+str(time.time() - starttime))
        return code
