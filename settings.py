import os
from sys import platform as _platform
##################################docker config#################################
docker_url_linux = "unix://var/run/docker.sock"
docker_url_other = "tcp://localhost:4243"

docker_url = docker_url_linux if _platform.lower().startswith("linux") else docker_url_other

#mapped_port_in = 80   # for apache
mapped_port_in = 8888 # for node
mapped_port_out = 49160

report_verbosity = "DEBUG"
spoiled_mode = False
browser_visible = False
timeout = 5
################################################################################

###################################file config##################################

current_path = os.path.dirname(os.path.realpath(__file__))

## results default folder
results_filename = current_path + "/reports/TestResults.csv"

##input dirs
applications_path = current_path + "/data/targets/applications/"
configurations_path = current_path + "/data/targets/configurations/"
containers_path = current_path + "/data/targets/containers/"
exploits_path = current_path + "/data/exploits/"

################################################################################
