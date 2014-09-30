#!/bin/bash

apt-get update

# install curl
apt-get -q -y install curl

# install docker 0.9.0
sh -c "curl https://get.docker.io/gpg | apt-key add -"
sh -c "echo deb http://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"
apt-get update
apt-get -q -y install lxc-docker

# install Python package manager
apt-get -q -y install python-pip

# install python bindings and other required software
pip install selenium
pip install docker-py
pip install pyvirtualdisplay
apt-get -q -y install xvfb
apt-get -q -y install cgroup-lite

# reboot the PC
reboot
