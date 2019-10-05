Wanderu Commander
#################

wanderu.commander is a tool that leverages ArgParse to discover and generate
command lines for programs.

Quick Setup
==========

1. install wanderu.commander (IE. pip or setup.py)::

   $ pip install wanderu.commander
   OR
   $ python setup.py develop
   OR
   $ python setup.py install

2. Make an entry point for your commands (Eg. mymod/main.py)::

    from wanderu.commander.main import Commander

    def main():
        desc = "Example 1 program description."
        version = "0.1"
        cmdr = Commander(prog="example1", module="mymod.commands",
                        desc=desc, version=version)
        res = cmdr.execute()  # read command line, parse, respond
        return res

3. Add commands programs to *mymod/commands/* (don't forget an __init__.py).
   IE. mymod/commands/command1.py

    Make a class name that is the same (case-insensitive) name as the 
    module name::

        @description("My command")
        @parameter(name="command1",
                   optional=False,
                   description="First command")
        class Command1(CommandBase):
            def execute(param1=None, **kwargs):
                print "executing Command1 with param1"

4. Add entry as setuptools endpoint so a script is created during install
(setup.py).::

    setup(
    ...
        entry_points={
            'console_scripts': [
                'myprog = mymod.main:main',
            ]
    ...
    )

 Install your module (IE. pip or setup.py), and run ``myprog --help``.
