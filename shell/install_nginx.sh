#!/bin/bash
# Install nginx
sudo apt install nginx
# Copy nginx.conf file to nginx folder
sudo cp /var/projectseven/web/nginx.conf /etc/nginx
# Restart Nginx
sudo service nginx restart

