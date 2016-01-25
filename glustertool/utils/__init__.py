import subprocess


class GlusterCmdExecuteFailed(Exception):
    pass


def execute(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return (p.returncode, out.strip(), err.strip())


def execute_gluster_cmd(cmd):
    cmd = ["gluster"] + cmd + ["--mode=script"]
    rc, out, err = execute(cmd)
    if rc != 0:
        raise GlusterCmdExecuteFailed(err)

    return out


def execute_gluster_cmd_xml(cmd):
    cmd += ["--xml"]
    out = execute_gluster_cmd(cmd)

    return out
