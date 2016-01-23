"""
gfid: Tool to get GFID of a file or directory
---------------------------------------------
Works both in Gluster Mount and in Backend.

    glustertool gfid <PATH>

For example,

    glustertool gfid /mnt/gv1/f1
    glustertool gfid /bricks/b2/f1
"""
import errno
import uuid
import xattr
import sys
import os


# For NetBSD/FreeBSD and Linux compatibility
if getattr(errno, "ENODATA"):
    ENODATA = errno.ENODATA
elif getattr(errno, "ENOATTR"):
    ENODATA = errno.ENOATTR
else:
    ENODATA = 87


def get_gfid(path):
    try:
        return uuid.UUID(bytes=xattr.get(path, "trusted.gfid",
                                         nofollow=True))
    except (IOError, OSError) as e:
        if e.errno == ENODATA:
            return uuid.UUID(bytes=xattr.get(path, "glusterfs.gfid",
                                             nofollow=True))
        else:
            raise


def cmdargs(p):
    p.add_argument("path", help="File/Directory path")


def run(args):
    try:
        print get_gfid(args.path)
    except (OSError, IOError) as e:
        print "[Error %s] %s" % (e.errno, os.strerror(e.errno))
        sys.exit(-1)
