#!/usr/bin/env python
"""
Extracts Volumes list from the given sosreport path and displays
"""
import os


def cmdargs(parser):
    # Add arguments for your tool using parser object
    # For example, parser.add_argument("--name", help="Name")
    parser.add_argument("path", help="Sosreport path")


def run(args):
    volsdir = os.path.join(args.path, "var/lib/glusterd/vols")

    for v in os.listdir(volsdir):
        print(v)
