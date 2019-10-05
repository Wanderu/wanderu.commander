# coding: utf-8

from wanderu.commander.commanddescription import description, parameter
from wanderu.commander.commandbase import CommandBase

from random import choice

@description("Play the game of Operation.")
@parameter(name="operation",
           optional=False,
           description="Operation to perform.",
           choices=['funnybone', 'brokenheart'])
class Operation(CommandBase):
    def execute(self, operation=None, **kwargs):
        print "Operating on: %s" % operation

        if not choice((True, False)):
            print "BBBBZZZZZZZZZZZZZZZZZZ. Steady those hands."
        else:
            print "Thank you Doctor. You get $100."
