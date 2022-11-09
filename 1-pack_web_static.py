#!/usr/bin/python3
"""pack files"""

from datetime import datetime
from fabric.api import run, local


def do_pack():
    """
    Gen tarball from web_static
    Return path if successfull, else None"""

    suffix = datetime.now().strftime("%Y%m%d%H%M%S")
    filePath = f"versions/web_static_{suffix}.tgz"

    # create versions folder
    local("mkdir -p versions/")

    # pack web_static
    tarball = local(f"tar -cvzf {filePath} web_static/")

    if tarball.succeeded:
        return filePath
