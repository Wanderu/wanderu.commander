"""
Description: Describe a command.
"""

'''
NOTE: collections.deque is used because decorators are applied from bottom to
top. We want semantics for positional arguments specified as
decorators from top to bottom to be matched left to right on the command line.
'''

from types import NoneType
from collections import deque

from enum import Enum


def description(value, extended=None):
    def dec(cl):
        cl.__description = value
        cl.__extended_desc = "" if extended is None else extended
        return cl
    return dec

def usage(value):
    def dec(cl):
        if not hasattr(cl, "__usage"):
            cl.__usage = deque()
        cl.__usage.appendleft(value)
        return cl
    return dec

def example(value):
    def dec(cl):
        if not hasattr(cl, "__examples"):
            cl.__examples = deque()
        cl.__examples.appendleft(value)
        return cl
    return dec

def parameter(name, description, optional=True, shortname=None, default=None,
                                 choices=None, action=None, type=NoneType):
    def dec(cl):
        if not hasattr(cl, "__parameters"):
            cl.__parameters = deque()
        cl.__parameters.appendleft(Param(name, description, optional,
                                         shortname, default, choices,
                                         action, type))
        return cl
    return dec

class Param(object):

    def __init__(self, name, description, optional=True, shortname=None,
                    default=None, choices=None, action=None, ptype=NoneType):
        super(Param, self).__init__()
        self.name = name
        self.shortname = shortname
        self.description = description
        self.optional = optional
        self.default = default
        self.choices = choices
        self.action = ParamAction.STORE.value if action is None else action
        # self.ptype = str if ptype is None else ptype
        self.ptype = ptype
        if type(self.ptype) is not type:
            raise TypeError("Expecting type of type type, found %s" \
                            % str(self.ptype))


# TODO: implement these convenience functions
class SingleParam(Param):

    def __init__(self, name, description, optional=True, shortname=None,
                 default=None, choices=None, action=None, ptype=NoneType):
        raise NotImplementedError("Not implemented.")

class MultiParam(Param):

    def __init__(self, name, description, optional=True, shortname=None,
                 default=None, choices=None, action=None, ptype=NoneType):
        raise NotImplementedError("Not implemented.")

class FlagParam(Param):

    def __init__(self, name, description, optional=True, shortname=None,
                 default=None, choices=None, action=None, ptype=NoneType):
        raise NotImplementedError("Not implemented.")

class ParamAction(Enum):
    STORE = "store"
    STORE_TRUE = "store_true"
    STORE_FALSE = "store_false"
    APPEND = "append"

if __name__ == "__main__":
    pass
