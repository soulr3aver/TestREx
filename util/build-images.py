#!/usr/bin/env python

import os
import subprocess

current_path = os.path.dirname(os.path.realpath(__file__))
containers_path = current_path + "/../data/targets/containers/"

for root, dirs, files in os.walk(containers_path):
    for container in dirs:
        p = subprocess.Popen(["docker", "build", "-t", "testbed/%s" % container, "."], cwd=containers_path+container)
        p.wait()
