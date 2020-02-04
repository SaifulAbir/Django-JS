#!/usr/bin/env bash
sudo apt update
sudo apt install python3 python python-minimal python3-pip python3-dev libmysqlclient-dev -y
pip3 install virtualenv
cd /var/
sudo mkdir projectseven
sudo chown ubuntu projectseven
sudo mkdir projectseven_static
sudo chown ubuntu projectseven_static
git checkout master
cd projectseven/web
virtualenv -p python3 venv
