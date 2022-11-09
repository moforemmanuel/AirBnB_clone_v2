#!/usr/bin/python3
"""
extract a .tgz archive from the contents of the web_static folder
Usage:
    fab -f 2-deploy_web_static.py do_deploy -i <identity-file>
"""
from fabric.api import local, put, run, env
from datetime import datetime
import os


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
    """Extract .tgz archive from the contents of /web_static
       returns True if successful and False if not
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
