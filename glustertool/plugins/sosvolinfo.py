#!/usr/bin/env python
"""
Extracts Volume info from the given sosreport path and displays
similar to gluster volume info command
"""
import os

vol_types = [
    "Distribute",
    "Stripe",
    "Replicate",
    "Striped-Replicate",
    "Disperse",
    "Tier",
    "Distributed-Stripe",
    "Distributed-Replicate",
    "Distributed-Striped-Replicate",
    "Distributed-Disperse"
]

transport_types = [
    "TCP",
    "RDMA",
    "TCP,RDMA"
]

vol_status = [
    "Created",
    "Started",
    "Stopped"
]


def get_type(type_code):
    return vol_types[int(type_code)]


def get_status(status_code):
    return vol_status[int(status_code)]


def get_transport_type(type_code):
    return transport_types[int(type_code)]


def print_volinfo(name, data):
    out = {"name": name}
    for line in data.split("\n"):
        line = line.strip()
        if not line:
            continue

        k, v = line.split("=", 1)
        out[k] = v

    print("Volume Name: %s" % out["name"])
    print("Type: %s" % get_type(out["type"]))
    print("Volume ID: %s" % out["volume-id"])
    print("Status: %s" % get_status(out["status"]))
    print("Snapshot Count: %s" % out.get("snapshot-count", 0))
    print("Number of Bricks: %s" % out["count"])
    print("Transport-type: %s" % get_transport_type(out["transport-type"]))
    print("Bricks:")
    for i in range(0, int(out["count"])):
        bname = "brick-%d" % i
        print("Brick%s: %s" % (i, out[bname]))

    print


def cmdargs(parser):
    # Add arguments for your tool using parser object
    # For example, parser.add_argument("--name", help="Name")
    parser.add_argument("path", help="Sosreport path")
    parser.add_argument("--name", help="Volume Name")


def run(args):
    volsdir = os.path.join(args.path, "var/lib/glusterd/vols")

    for v in os.listdir(volsdir):
        # If volume name is specified
        if args.name is not None and args.name != v:
            continue

        info_file = os.path.join(volsdir, v, "info")
        volinfo = None
        with open(info_file) as f:
            volinfo = f.read()

        if volinfo is not None:
            print_volinfo(v, volinfo)
