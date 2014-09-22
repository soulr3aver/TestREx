#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.dirname(".."))
import settings
from ExecutionEngine import ExecutionEngine

if __name__ == "__main__":

    bugbox_exploits = os.listdir(settings.exploits_path+"bugbox/")
    bugbox_exploits.remove(".DS_Store")
    bugbox_exploits.remove(".DS_Storec")
    bugbox_exploits.remove("__init__.py")
    bugbox_exploits.remove("framework")
    
    for file in bugbox_exploits:
        if file.find(".pyc"):
            bugbox_exploits.remove(file)
    
    bugbox_exploits = [settings.exploits_path+"bugbox/"+filename for filename in bugbox_exploits]

    ex = ExecutionEngine()

    for exploit_path in bugbox_exploits:

        exploit_file = open(exploit_path)

        target = ""

        for line in exploit_file.readlines():
            if (line.find("'Target'") != -1):
                target = line.split("\"")[-2]
            if (line.find("'Plugin'") != -1):
                target +="_"+line.split("\"")[-2]
                
        target = target.replace(" ", "_").replace(".","_").lower()

        configuration = settings.configurations_path+target+"__ubuntu-apache-mysql"

        print("RUNNNG BUGBOX EXPLOIT")
        print("configuration: " + configuration)
        print("bugbox_exploit: " + exploit_path)

        ex.run(configuration, exploit_path, settings.report_path)

        print("EXPLOIT FINISHED")