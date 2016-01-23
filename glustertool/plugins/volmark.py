#!/usr/bin/env python
"""
To get Volmark from Master Volume,

Mount the Master Volume with Client PID -1, For example,

glusterfs --aux-gfid-mount --acl --volfile-server=localhost \\
    --volfile-id=gv1 --client-pid=-1 /mnt/gv1

    glustertool volmark <MOUNT_PATH>

For example,

    glustertool volmark /mnt/gv1

To get Volume Mark from Slave,

    glustertool volmark <MOUNT_PATH>

For example,

    glustertool volmark /mnt/gv2

"""
import struct
import xattr
import uuid
from errno import ENODATA
from datetime import datetime
import os
import sys


def human_time(ts):
    return datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d %H:%M:%S")


def cmdargs(parser):
    parser.add_argument("path", help="Mount Point Path")


def run(args):
    # Volmark from Master side
    fmt_string = "!" + "B" * 19 + "II"
    try:
        vm = struct.unpack(fmt_string, xattr.get(
            args.path,
            "trusted.glusterfs.volume-mark",
            nofollow=True))
        print "UUID        : %s" % uuid.UUID(
            "".join(['%02x' % x for x in vm[2:18]]))
        print "VERSION     : %s.%s" % vm[0:2]
        print "RETVAL      : %s" % vm[18]
        print "VOLUME MARK : %s.%s (%s)" % (
            vm[19], vm[20], human_time("%s.%s" % (vm[19], vm[20])))
    except (OSError, IOError) as e:
        if e.errno == ENODATA:
            pass
        else:
            print "[Error %s] %s" % (e.errno, os.strerror(e.errno))
            sys.exit(-1)

    # Volmark from slave side
    all_xattrs = xattr.list(args.path)
    fmt_string = "!" + "B" * 19 + "II" + "I"
    volmark_xattrs = []
    for x in all_xattrs:
        if x.startswith("trusted.glusterfs.volume-mark."):
            volmark_xattrs.append(x)

    for vx in volmark_xattrs:
        try:
            vm = struct.unpack(fmt_string, xattr.get(
                args.path,
                vx))

            print "UUID        : %s" % uuid.UUID(
                "".join(['%02x' % x for x in vm[2:18]]))
            print "VERSION     : %s.%s" % vm[0:2]
            print "RETVAL      : %s" % vm[18]
            print "VOLUME MARK : %s.%s (%s)" % (
                vm[19], vm[20], human_time("%s.%s" % (vm[19], vm[20])))
            print "TIMEOUT     : %s (%s)" % (vm[-1], human_time(vm[-1]))
        except (OSError, IOError) as e:
            if e.errno == ENODATA:
                pass
            else:
                print "[Error %s] %s" % (e.errno, os.strerror(e.errno))
                sys.exit(-1)
