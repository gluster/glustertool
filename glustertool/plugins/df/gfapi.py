import ctypes
from ctypes.util import find_library
import os

_api = None


class StatVfsData (ctypes.Structure):
    """
    statvfs structure, man statvfs to get the structure
    """
    _fields_ = [
        ('f_bsize', ctypes.c_ulong),
        ('f_frsize', ctypes.c_ulong),
        ('f_blocks', ctypes.c_ulong),
        ('f_bfree', ctypes.c_ulong),
        ('f_bavail', ctypes.c_ulong),
        ('f_files', ctypes.c_ulong),
        ('f_ffree', ctypes.c_ulong),
        ('f_favail', ctypes.c_ulong),
        ('f_fsid', ctypes.c_ulong),
        ('f_flag', ctypes.c_ulong),
        ('f_namemax', ctypes.c_ulong),
        ('__f_spare', ctypes.c_int * 6),
    ]


def _lazy_init_libgfapi():
    """
    Loads ctypes library only if not loaded already
    """
    global _api
    if not _api:
        _api = ctypes.CDLL(find_library("gfapi"), ctypes.RTLD_GLOBAL)


def _mount_gluster_volume(volume, host, port, protocal):
    """
    Mounts GlusterFS volume
    """
    fs = _api.glfs_new(volume)
    _api.glfs_set_volfile_server(fs, protocal, host, port)
    _api.glfs_init(fs)
    return fs


def _umount_gluster_volume(fs):
    """
    Unmounts GlusterFS volume
    """
    _api.glfs_fini(fs)


def statvfs(volume, host='localhost', port=24007, protocal='tcp'):
    _lazy_init_libgfapi()
    data = StatVfsData()
    _api.glfs_statvfs.restype = ctypes.c_int
    _api.glfs_statvfs.argtypes = [ctypes.c_void_p,
                                  ctypes.c_char_p,
                                  ctypes.POINTER(StatVfsData)]
    fs = _mount_gluster_volume(volume, host, port, protocal)
    rc = _api.glfs_statvfs(fs, "/", ctypes.byref(data))

    # To convert to os.statvfs_result we need to pass tuple/list in
    # following order: bsize, frsize, blocks, bfree, bavail, files
    # ffree, favail, flag, namemax
    return os.statvfs_result((data.f_bsize,
                              data.f_frsize,
                              data.f_blocks,
                              data.f_bfree,
                              data.f_bavail,
                              data.f_files,
                              data.f_ffree,
                              data.f_favail,
                              data.f_flag,
                              data.f_namemax))
