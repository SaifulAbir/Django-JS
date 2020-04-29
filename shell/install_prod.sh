#!/usr/bin/env bash

############################################################
################ P R E R E Q U I S I T E S #################
############################################################
# Getting the source code:
#
# cd /var/
# sudo mkdir p7
# sudo chown ubuntu p7
# git clone https://mahadi_ish@bitbucket.org/p7_team/p7_repo.git p7
############################################################

sudo apt update
sudo apt install python3 python python-minimal python3-pip python3-dev libmysqlclient-dev -y
pip3 install virtualenv
cd /var/
sudo mkdir p7_static
sudo chown ubuntu p7_static
git checkout master
cd p7
virtualenv -p python3 venv
