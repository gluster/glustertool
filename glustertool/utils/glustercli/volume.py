from glustertool.utils import execute_gluster_cmd


def _action(volname, action, force=False):
    cmd = ["volume", action, volname]
    if force:
        cmd += ["force"]

    execute_gluster_cmd(cmd)


def create(volname, bricks, replica=0, stripe=0, arbiter=0,
           disperse=0, disperse_data=0, redundancy=0,
           transport="tcp", force=False):
    cmd = ["volume", "create", volname]
    if replica > 0:
        cmd += ["replica", replica]

    if stripe > 0:
        cmd += ["stripe", stripe]

    if arbiter > 0:
        cmd += ["arbiter", arbiter]

    if disperse > 0:
        cmd += ["disperse", disperse]

    if disperse_data > 0:
        cmd += ["disperse-data", disperse_data]

    if redundancy > 0:
        cmd += ["redundancy", redundancy]

    cmd += ["transport", transport]

    cmd += bricks
    if force:
        cmd += ["force"]

    return execute_gluster_cmd(cmd)


def delete(volname):
    _action(volname, "delete")


def start(volname, force=False):
    _action(volname, "start", force)


def stop(volname, force=False):
    _action(volname, "stop", force)


def restart(volname, force=False):
    _action(volname, "stop", force)
    _action(volname, "start", force)


def setopt(volname, key, value):
    cmd = ["volume", "set", volname, key, value]
    execute_gluster_cmd(cmd)


def resetopt(volname, key=None, force=False):
    cmd = ["volume", "reset", volname]
    if key is not None:
        cmd += [key]

    if force:
        cmd += ["force"]

    execute_gluster_cmd(cmd)


def getopt():
    pass


def info():
    pass


def status():
    pass
