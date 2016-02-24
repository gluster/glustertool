#!/usr/bin/env python
"""
dirgfid2path: To convert directory GFID to Path

Usage:

    glustertool dirgfid2path <BRICK_PATH> <GFID>

Example:

    glustertool dirgfid2path /bricks/b1 \
        619c9de3-261b-47be-af2d-0754f3e2f578
"""
import os

ROOT_GFID = "00000000-0000-0000-0000-000000000001"


def symlink_gfid_to_path(brick, gfid):
    """
    Each directories are symlinked to file named GFID
    in .glusterfs directory of brick backend. Using readlink
    we get PARGFID/basename of dir. readlink recursively till
    we get PARGFID as ROOT_GFID.
    """
    if gfid == ROOT_GFID:
        return ""

    out_path = ""
    while True:
        path = os.path.join(brick, ".glusterfs", gfid[0:2], gfid[2:4], gfid)
        path_readlink = os.readlink(path)
        pgfid = os.path.dirname(path_readlink)
        out_path = os.path.join(os.path.basename(path_readlink), out_path)
        if pgfid == "../../00/00/%s" % ROOT_GFID:
            break
        gfid = os.path.basename(pgfid)
    return out_path


def cmdargs(parser):
    parser.add_argument("brick", help="Brick Path")
    parser.add_argument("gfid", help="GFID of a directory")


def run(args):
    try:
        print (symlink_gfid_to_path(args.brick, args.gfid))
    except (OSError, IOError) as e:
        print ("ERROR: {0}".format(e))
