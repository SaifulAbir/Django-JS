#!/usr/bin/env bash
sudo apt update
sudo apt install python3 python3-pip -y
pip3 install virtualenv
virtualenv -p python3 venv