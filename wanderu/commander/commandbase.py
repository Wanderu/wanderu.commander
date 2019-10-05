######################
# Description:
# Base class for all commands.
# This does not support parameter inheritance.
######################

from wanderu.commander import userutils
from wanderu.commander.commanddescription import (parameter,
                                                  ParamAction)

from collections import deque


class CommandMeta(type):
    """
    Use this metaclass for command inheritance.
    To use, create a subclass of CommandBase and set on its class:
        __metaclass__ = CommandMeta

    Command parameter inheritance will work after this.
    See rediscrape.command (rediscrape/command.py) for a examples.
    """
    def __init__(cls, class_name, bases, attrs):
        setattr(cls, "__parameters", deque())
        super(CommandMeta, cls).__init__(class_name, bases, attrs)
        cls_params = getattr(cls, '__parameters')
        for base in bases:
            cls_params.extendleft(getattr(base, '__parameters', []))


class AbstractCommand(object):
    """This is used by the system to discover and identify a command.
    All commands must be a subclass of this class.
    """
    def execute(self, **kwargs):
        raise NotImplemented("Not implemented.")


class CommandBase(AbstractCommand):
    # implements(ICommand)

    def __init__(self, *args, **kwargs):
        self.verbose = False

    def parse_args(self, **kwargs):
        # Run pre_execute for all base classes (init inherited parameters)
        for Cls in self.__class__.mro():
            if hasattr(Cls, "pre_execute"):
                _code = Cls.pre_execute(self, **kwargs)
                if _code > 0:
                    return _code

    def execute(self, verbose=False, **kwargs):
        self.verbose = verbose
        return 0

    def prompt(self, msg):
        return userutils.query_yes_no(msg)

    def __getitem__(self, item):
        raise AttributeError(item+" does not exist.")

    def __getparam__(self, name):
        try:
            for param in self.__class__.__dict__['__parameters']:
                if param.name == name:
                    return param
        except:
            pass
        return None

@parameter(name="yes", shortname="y",
           description="Answer yes to all prompts.",
           optional=True,
           action=ParamAction.STORE_TRUE.value,
           default=False,
           type=bool)
class YesCommand(object):
    def pre_execute(self, yes=False, **kwargs):
        self.yes = yes
        return 0

