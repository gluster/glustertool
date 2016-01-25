# glustertool - Collection of Gluster Tools

`glustertool` is a meta tool for running other Gluster tools. This
provides infrastructure to add utility/debugging tools for Gluster.

## Install

Clone the repo and install `glustertools` using `python setup.py install`.

## Usage
Tools can be accessed using

    glustertool TOOLNAME ARGS..

To see the list of tools available,

    glustertool list

To see the documentation of available tools,

    glustertool doc [TOOLNAME]

For tool help,

    glustertool TOOLNAME --help

Refer [CONTRIBUTING.md](CONTRIBUTING.md), if you are interested in creating tools/plugins for glustertool.

## TODO
1. Plugins dependency management
2. RPM/DEB and BSD Port
