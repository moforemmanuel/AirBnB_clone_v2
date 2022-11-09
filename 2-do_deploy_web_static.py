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
from datetime import datetime
from fabric.api import env, put, run, local

env.user = "ubuntu"
env.hosts = ["34.75.10.160", "35.231.86.187"]


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

    try:
        # archive_path=versions/web_static_20170315003959.tgz
        tarball = archive_path.split("/")[-1]
        tar_no_ext = tarball.split(".")[0]
        # tar_folder = archive_path.split("/")[-2]

        # upload file to /tmp/
        put(archive_path, "/tmp/")

        # decompress
        run(f"mkdir -p /data/web_static/releases/{tar_no_ext}/")
        run(f"tar -xzf /tmp/{tarball} -C /data/web_static/releases/{tar_no_ext}")

        # delete archive
        run(f"rm /tmp/{tarball}")

        # delete symlink /data/web_static/current
        run(f"mv /data/web_static/releases/{tar_no_ext}/web_static/* /data/web_static/releases/{tar_no_ext}/")
        run(f"rm -rf /data/web_static/releases/{tar_no_ext}/web_static")
        run("rm -rf /data/web_static/current")

        # recreate symlink /data/web_static/current
        # link to /data/web_static/releases/<archive filename without extension>
        run(
            "ln -s /data/web_static/releases/{tar_no_ext}/ /data/web_static/current")
        run("echo 'New version deployed!'")
        return True

    except:
        return False
