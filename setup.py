# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="glustertool",
    version="0.1.1",
    packages=["glustertool"],
    include_package_data=True,
    install_requires=['argparse', 'pyxattr'],
    entry_points={
        "console_scripts": [
            "glustertool = glustertool.cli:main"
        ]
    },
    platforms="linux",
    zip_safe=False,
    author="Aravinda VK",
    author_email="avishwan@redhat.com",
    description="Gluster Tools",
    license="",
    keywords="gluster, cli, tools",
    url="https://github.com/aravindavk/glustertool",
)
