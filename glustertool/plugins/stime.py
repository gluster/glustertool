#!/usr/bin/env python
"""
To get stime of a file or dir from brick backend

glustertool stime <MASTER UUID> <SLAVE UUID> <PATH>

For example,

glustertool stime 346d1076-05b6-4a59-9947-1e7d31a66294 \
     169b8fbd-e1ec-419d-af63-215eaf69d621 /bricks/b2

"""
import struct
import xattr
import os
import sys


def cmdargs(parser):
    parser.add_argument("master_uuid", help="Master Volume UUID")
    parser.add_argument("slave_uuid", help="Slave Volume UUID")
    parser.add_argument("path", help="Path")


def run(args):
    try:
        stime_key = "trusted.glusterfs.%s.%s.stime" % (args.master_uuid,
                                                       args.slave_uuid)
        print struct.unpack("!II", xattr.get(args.path, stime_key,
                                             nofollow=True))
    except (OSError, IOError) as e:
        sys.stderr.write("[Error %s] %s\n" % (e.errno, os.strerror(e.errno)))
        sys.exit(-1)
