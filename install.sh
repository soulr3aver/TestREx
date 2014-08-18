#!/bin/bash

apt-get update
apt-get -q -y install curl
sh -c "curl https://get.docker.io/gpg | apt-key add -"
sh -c "echo deb http://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"
apt-get update
apt-get -q -y install lxc-docker-0.9.0
apt-get -q -y install python-pip
pip install selenium
pip install docker-py
apt-get -q -y install cgroup-lite
reboot

