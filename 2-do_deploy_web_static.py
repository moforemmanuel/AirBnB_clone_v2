#!/usr/bin/python3
"""
Distributes archived pack to both web servers
Usage:
    fab -f 2-do_deploy_web_static.py do_deploy:
    archive_path=versions/<file_name> -i my_ssh_private_key

Example:
    fab -f 2-do_deploy_web_static.py do_deploy:
    archive_path=versions/web_static_20170315003959.tgz -i my_ssh_private_key
"""

import os.path
from fabric.api import env, put, run

env.hosts = ["3.233.229.162", "44.197.235.170"]
env.user = "ubuntu"


def do_pack():
    """Generates .tgz archive from the contents of /web_static
       returns archive's path if successful and None if not
    """
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    filePath = 'versions/web_static_{}.tgz'.format(now)

    local('mkdir -p versions/')
    createArchive = local('tar -cvzf {} web_static/'.format(filePath))

    if createArchive.succeeded:
        return filePath
    return None

def do_deploy(archive_path):
    """Distributes an archive to a web server.
       Returns True if successful and false otherwise
    """
    if not os.path.exists(archive_path):
        return False
