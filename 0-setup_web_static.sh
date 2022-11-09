#!/usr/bin/env bash
# Script to set up web servers for deployment

# install nginx
sudo apt update
sudo apt install nginx

# create dirs, check if exist
mkdir -p /data/
mkdir -p /data/web_static/
mkdir -p /data/web_static/releases/
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

# generate fake html
printf %s "
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
" > /data/web_static/releases/test/index.html

# symlink, override if exist
ln -sf /data/web_static/releases/test/ /data/web_static/current

# chown to ubuntu Recursively
chown -R ubuntu:ubuntu /data/

# update nginx config to serve webstatic current folder using alias
printf %s "server {
	listen 80 default_server;
	listen [::]:80 default_server;
	add_header X-Served_By $HOSTNAME;
	root /var/www/html;
	index index.html;

	location /hbnb_static/ {
		alias /data/web_static/current/;
		index index.html index.htm;
	}
}" | sudo tee /etc/nginx/sites-available/default

# restart nginx
sudo service nginx restart
