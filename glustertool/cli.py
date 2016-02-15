"""
glustertool: Collection of Gluster utilities
--------------------------------------------

To see the list of available tools,

glustertool list

To view documentation of the tool,

glustertool doc [<TOOLNAME>]

For Tool help,

glustertool <TOOLNAME> --help
"""

import os
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import json

from glustertool.utils import execute


SUBCMD_DIR = "plugins"
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
SUBCMD_DIR = os.path.join(CUR_DIR, SUBCMD_DIR)


def load_plugin(plugin):
    return __import__("glustertool.plugins.{0}".format(plugin),
                      fromlist=[plugin])


def parse_tool_json(path):
    return json.load(open(path))


def handle_list():
    print ("List of available tools, `glustertool doc <TOOLNAME>` "
           "or `glustertool <TOOLNAME> -h` for more details about the tool.")
    for d in sorted(os.listdir(SUBCMD_DIR)):
        if d.startswith("__init__"):
            continue

        if d.endswith(".pyc") or d.endswith(".pyo"):
            continue

        if d.endswith(".py"):
            d = d.replace(".py", "")

        print (d)


def handle_doc(subcommand=None):
    if subcommand is None:
        print (__doc__)
    else:
        try:
            submodule = load_plugin(subcommand)
            print (submodule.__doc__)
        except ImportError:
            tool_dir = os.path.join(SUBCMD_DIR, subcommand)
            tool_json = os.path.join(tool_dir, "tool.json")
            tool_doc = os.path.join(tool_dir, "doc.txt")
            if os.path.exists(tool_json):
                if os.path.exists(tool_doc):
                    print (open(tool_doc).read())
            else:
                sys.stderr.write("Invalid Command\n")
                sys.exit(1)


def main():
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=__doc__)
    subparsers = parser.add_subparsers(dest="mode")
    if len(sys.argv) == 1:
        print (__doc__)
        return

    subcommand = sys.argv[1]
    if subcommand == "doc":
        name = sys.argv[2] if len(sys.argv) == 3 else None
        return handle_doc(name)

    if subcommand == "list":
        return handle_list()

    try:
        submodule = load_plugin(subcommand)
        p = subparsers.add_parser(subcommand, add_help=False)
        submodule.cmdargs(p)
        p.add_argument("--help", action="help",
                       help="show this help message and exit")
        args = parser.parse_args()
        submodule.run(args)
    except ImportError:
        tool_dir = os.path.join(SUBCMD_DIR, subcommand)
        tool_json = os.path.join(tool_dir, "tool.json")
        if os.path.exists(tool_json):
            tool_data = parse_tool_json(tool_json)
            cmd = [tool_data["prog"]] if tool_data["prog"] else []
            cmd += [os.path.join(tool_dir, tool_data["bin"])]
            cmd += sys.argv[2:]
            rc, out, err = execute(cmd)
            if rc == 0:
                sys.stdout.write(out)
                sys.exit(0)
            else:
                sys.stderr.write(err)
                sys.exit(rc)
        else:
            sys.stderr.write("Invalid Command\n")
            sys.exit(1)


if __name__ == "__main__":
    main()
