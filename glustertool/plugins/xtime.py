#!/usr/bin/env python
"""
To get xtime of a file or dir from brick backend,

glustertool xtime <VOLUME UUID> <PATH>

For example,

glustertool xtime 346d1076-05b6-4a59-9947-1e7d31a66294 /bricks/b2/f1

"""
import struct
import xattr
import sys
import os


def cmdargs(parser):
    parser.add_argument("vol_uuid", help="Volume UUID", metavar="UUID")
    parser.add_argument("path", help="Path", metavar="PATH")


def run(args):
    xtime_key = "trusted.glusterfs.%s.xtime" % args.vol_uuid
    try:
        print struct.unpack("!II", xattr.get(args.path, xtime_key,
                                             nofollow=True))
    except (OSError, IOError) as e:
        print "[Error %s] %s" % (e.errno, os.strerror(e.errno))
        sys.exit(-1)
