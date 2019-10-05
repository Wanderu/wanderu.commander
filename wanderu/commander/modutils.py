######################
# Description:
# Various module utils.
######################

import os
import pkgutil
import inspect

# fetch a list of modules within a package.
# exclude modules specified in exclude.
from wanderu.commander.commandbase import AbstractCommand


def get_package_modules(package_path, exclude=None):
    try:
        mod = __import__(".".join(package_path), fromlist=package_path[:-1])
        pkgpath = os.path.dirname(mod.__file__)
        modnames = [name for _, name, _ in pkgutil.iter_modules([pkgpath])]
        if exclude is not None:
            modnames = filter(lambda modname: modname not in exclude, modnames)
        return modnames
    except ImportError:
        return []

def find_module(module_path, exclude=None, case_sensitive=False):
    name = module_path[-1]
    mods = get_package_modules(module_path[:-1], exclude)
    for othername in mods:
        if case_sensitive:
            if othername.lower() == name.lower():
                return othername
        else:
            if othername == name:
                return othername
    return None

def get_module(*module_path):
    # print("get_module: %s" % str(module_path))
    try:
        return __import__(".".join(module_path), fromlist=module_path[:-1])
    except ImportError:
        return None

def get_module_cls(*module_path):
    mod_name = find_module(module_path)
    if mod_name is not None:
        print "importing: "
        print ".".join(module_path), "fromlist:", module_path[:-1]
        command_mod = __import__(".".join(module_path),
                                 fromlist=module_path[:-1])
        command_clsname = mod_name
        for key, value in command_mod.__dict__.items():
            if key.lower() == mod_name:
                command_clsname = key
        command_cls = getattr(command_mod, command_clsname)
        return command_cls
    else:
        return None

# Expects module name to equal class name (case-insensitive).
def get_command_cls(*module_path):
    mod_name = module_path[-1]
    mod = get_module(*module_path)
    if not mod:
        return None

    for key, value in mod.__dict__.items():
        if inspect.isclass(value):
            if issubclass(value, AbstractCommand) \
                    and key.lower() == mod_name.lower():
                return value
    return None
