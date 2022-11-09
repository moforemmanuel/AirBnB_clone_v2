#!/usr/bin/python3
"""pack files"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """returns the archive path if the archive has been correctly generated"""
    suffix = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = f"versions/web_static_{suffix}.tgz"

    # create versions folder
    local("mkdir -p versions/")

    # pack web_static
    tarball = local(f"tar -cvzf {file_path} web_static/")

    if tarball.succeeded:
        return file_path
