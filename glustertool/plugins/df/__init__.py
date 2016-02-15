#!/usr/bin/env python
"""
Write your tool documentation here
"""
import argparse


FIELDS = {
    "volume": "Volume",
    "itotal": "Inodes",
    "iused": "IUsed",
    "iavail": "IFree",
    "ipcent": "IUse%",
    "size": "Size",
    "used": "Used",
    "avail": "Avail",
    "pcent": "Use%",
    "status": "Status",
    "type": "Type",
    "num_bricks": "Bricks"
}


def cmdargs(parser):
    # Add arguments for your tool using parser object
    # For example, parser.add_argument("--name", help="Name")

    parser.add_argument('-B', '--block-size',
                        help="scale sizes by SIZE before printing them.  \
                        E.g., '-BM' prints sizes in units of 1,048,576 bytes. \
                        See SIZE format below.",
                        type=str, default='')
    parser.add_argument('-k', help="like --block-size=1K",
                        action='store_true', dest="onek")
    parser.add_argument('-h', '--human-readable', action='store_true',
                        help="print sizes in human readable format \
                        (e.g., 1K 2M 2G)")
    parser.add_argument('-H', '--si', action='store_true',
                        dest='human_readable_1000',
                        help="likewise, but use powers of 1000 not 1024")
    parser.add_argument('--total',
                        help="produce a grand total", action='store_true')
    parser.add_argument('-i', '--inodes', action='store_true',
                        help="list inode information instead of block usage")
    parser.add_argument('--status', help="Status to filter",
                        type=str, default='')
    parser.add_argument('--json', help="JSON Output", action='store_true')

    # Derived values
    parser.add_argument('--block-size-number', help=argparse.SUPPRESS,
                        default=1)
    parser.add_argument('--hr-block-size', help=argparse.SUPPRESS,
                        default=1024)
    parser.add_argument('--fields', help=argparse.SUPPRESS,
                        default="volume,type,num_bricks,status,size,used,\
                        avail,pcent")

    parser.add_argument('volume', help="Volume Name", nargs="?")


def run(args):
    print args

    return
    filters = {
        "name": args.name,
        "status": args.status,
        "type": args.type,
        "volumewithbrick": args.volumewithbrick
    }

    try:
        gvols = volumes.search(filters)
    except volumes.GlusterVolumeInfoFailed:
        msg = 'Error fetching gluster volumes details\n'
        sys.stderr.write(utils.color_txt(msg,
                                         'RED'))
        exit(1)

    if args.onek:
        args.block_size = 'K'

    if args.block_size != '':
        args.human_readable = False
        args.human_readable_1000 = False

    args.hr_block_size = 1000 if args.human_readable_1000 else 1024
    args.block_size_number = _get_block_size(args)

    if args.inodes:
        args.fields = "volume,type,num_bricks,status,itotal,\
        iused,iavail,ipcent"

    _display(gvols, args)
