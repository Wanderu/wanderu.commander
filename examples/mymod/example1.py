# coding: utf-8

from wanderu.commander.main import Commander

def main():
    desc = "Example 1 program description."
    version = "0.1"
    #           program name, module command location
    cmdr = Commander(prog="example1", module="mymod.commands",
                     desc=desc, version=version)
    res = cmdr.execute()  # read command line, parse, respond
    return res

if __name__ == "__main__":
    main()
