#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Why?

Converts this

GlusterFS Changelog | version: v1.1 | encoding : 2
E0b99ef11-4b79-4cd0-9730-b5a0e8c4a8c0^@4^@16877^@0^@0^@00000000-0000-0000-0000-
000000000001/dir1^@Ec5250af6-720e-4bfe-b938-827614304f39^@23^@33188^@0^@0^@0b99
ef11-4b79-4cd0-9730-b5a0e8c4a8c0/hello.txt^@Dc5250af6-720e-4bfe-b938-827614304f
39^@Dc5250af6-720e-4bfe-b938-827614304f39^@


to human readable :)

E 0b99ef11-4b79-4cd0-9730-b5a0e8c4a8c0 MKDIR 16877 0 000000000-0000-0000-0000
  -000000000001/dir1
E c5250af6-720e-4bfe-b938-827614304f39 CREATE 33188 0 0 0b99ef11-4b79-4cd0-9730
  -b5a0e8c4a8c0/hello.txt
D c5250af6-720e-4bfe-b938-827614304f39
D c5250af6-720e-4bfe-b938-827614304f39

Usage:

glustertool changelogparse <CHANGELOG_FILE>

For example,

glustertool changelogparse /bricks/b1/.glusterfs/changelogs/CHANGELOG.1439463377

"""
import sys
import os

from glustertool.utils import changelog


def cmdargs(parser):
    parser.add_argument("path", help="Changelog File Path")


def run(args):
    if os.path.exists(args.path):
        changelog.parse(args.path)
    else:
        sys.stderr.write("Invalid Changelog file\n")
        sys.exit(1)
