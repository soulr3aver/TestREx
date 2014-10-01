import docker
import imp
import os
import shutil
import signal
import sys
import time
import traceback
import settings
import glob
import subprocess

class ExecutionEngine():

    def __init__(self):
        self.docker_client = docker.Client(base_url=settings.docker_url, timeout=10)
        self.docker_containers = []
        self.docker_images = []
        self.config_files = []

    def run_batch_single(self, image_path):
        is_spoiled = False
        try:
            for file_ in glob.glob(settings.exploits_path+"*.py"):
                if (os.path.basename(file_) == "__init__.py"):
                    continue
                module_ = imp.load_source("Exploit", file_)
                class_ = getattr(module_, "Exploit")
                instance = class_()

                if (not hasattr(instance, "attributes") or not "Target" in instance.attributes.keys()):
                    continue

                target = instance.attributes["Target"]
                image_name = os.path.basename(image_path).split("__")[0]
                if ((target != None) and (target == image_name)):
                    try:
                        if (not settings.spoiled_mode):
                            self.run(image_path, file_)
                        else:
                            if (not is_spoiled):
                                self.run_application(image_path)
                                is_spoiled = True
                            self.inject_exploits(file_)
                    except:
                        self.print_engine_exception()
        finally:
            self.clean_environment()

    def run_batch(self):
        for image_path in glob.glob(settings.configurations_path + "/*"):
            self.run_batch_single(image_path)

    #runs the execution engine, with a given configuration (app+container)
    #and exploit, writes a report and cleans the environment
    def run(self, app_config, exploit):
        try:
            configuration_path = os.path.join(settings.configurations_path, app_config)
            exploit_path = os.path.join(settings.exploits_path, exploit)
            self.run_application(configuration_path)
            self.inject_exploits(exploit_path)
        except:
            self.print_engine_exception()
        finally:
            self.clean_environment()


    #runs an application for manual interaction and waits for the Ctrl+C signal
    #to clean the environment
    def run_manual(self, app_config):
        try:
            self.run_application(os.path.join(settings.configurations_path, app_config))
            signal.signal(signal.SIGINT, self.signal_handler)
            print("...the application is up and running!\nPress Ctr+C to stop the image...")
            signal.pause()
        except:
            self.print_engine_exception()

    #run an application in a given container
    def run_application(self, configuration_path):
        configuration_name = os.path.basename(configuration_path)
        application_name = configuration_name.split("__")[0]
        application_path = settings.applications_path + application_name
        image_name = "testbed/" + configuration_name

        print("Running '%s' application with container '%s'..." % (application_name, image_name))

        image_exists = False
        try:
            self.docker_client.images(name=image_name)[0]
            image_exists = True
        except:
            pass

        if (settings.disposable):
            if (image_exists):
                print("Removing the old persistent image...")
                self.docker_client.remove_image(image_name)
            self.build_image(configuration_path, application_path, image_name)
            self.docker_images.append(image_name)
        else:
            if (not image_exists):
                self.build_image(configuration_path, application_path, image_name)

        container_id = self.start_container(image_name)
        self.docker_containers.append(container_id)
        time.sleep(5)

    
    def build_image(self, config_path, app_path, image_name):
        print("Copying the application files...")
        for _file in os.listdir(config_path):
            self.config_files.append(app_path+"/"+_file)
            shutil.copy(config_path+"/"+_file, app_path)
        print("Building the '%s' image..." % image_name)
        p = subprocess.Popen(["docker", "build", "-t", image_name, "."], cwd=app_path)
        p.wait()
  
    def start_container(self, image_name):
        container_id = self.docker_client.create_container(image_name, ports=[8888])
        self.docker_client.start(container_id, port_bindings={settings.mapped_port_in:settings.mapped_port_out}, dns="8.8.8.8")
        return container_id

    def inject_exploits(self, exploit_path):
        #EXPERIMENTAL: run BugBox eploits -- replace their urls with our mapped ports and then
        #load the exploit
        exploitClassName = "Exploit"
        if ("bugbox" in exploit_path):
            exploit = open(exploit_path,'r')
            exploit_temp_path = exploit_path.replace(".py", "_temp.py")
            exploit_temp = open(exploit_temp_path,'w')

            for line in exploit.readlines():
                new_line = line.replace("localhost", "localhost:"+str(settings.mapped_port_out))
                new_line = new_line.replace("127.0.0.1", "localhost:"+str(settings.mapped_port_out))
                exploit_temp.write(new_line)

            exploit.close()
            exploit_temp.close()

            sys.path.append(os.path.dirname(exploit_temp_path))
            exploitModule = imp.load_source(exploitClassName, exploit_temp_path)

        else:
            exploitModule = imp.load_source(exploitClassName, exploit_path)

        exploitClass = getattr(exploitModule, exploitClassName)
        exploitInstance = exploitClass()

        if ("bugbox" in exploit_path):
            exploitInstance.exploit()
            self.normalize_bugbox_info(exploitInstance)
        else:
            exploitInstance.exploit(settings.report_verbosity)
            self.write_log(exploitInstance.__class__.__name__, exploitInstance.Log)
        self.write_testrun_info(exploitInstance, settings.results_filename)

    def normalize_bugbox_info(self, instance):
        result = "SUCCESS" if (instance.verify()) else "FAILURE"
        instance.result = result
        instance.attributes["Container"] = "ubuntu-apache-mysql"
        instance.time_spent = "N/A"
        instance.startup_ok = "SUCCESS"

    #writes the collected data into a report
    def write_log(self, filename, log):
        reports_folder = settings.current_path + "/reports"
        if not os.path.exists(reports_folder):
            os.makedirs(reports_folder)
        _file = open(reports_folder + "/%s.log" % filename, "a+")
        _file.write(log.getvalue())
        _file.close()

    def write_testrun_info(self, instance, filename):
        attributes = instance.attributes
        result = instance.result
        time_spent = instance.time_spent
        startup_ok = instance.startup_ok
        spoiled_mode = "CLEAN" if not settings.spoiled_mode else "SPOILED"
        _file = open(filename, "a+")
        csv = "%s, %s, %s, %s, %s, %s, %s, %s, Exploits for \"%s\"\n" % (
                   attributes["Name"],
                   attributes["Target"],
                   attributes["Container"],
                   attributes["Type"],
                   spoiled_mode,
                   startup_ok,
                   result,
                   time_spent,
                   attributes["Description"])
        _file.write(csv)
        _file.close()
        print("Results are saved to: %s" % filename)

    #cleans the execution environment (containers, images and conf files)
    def clean_environment(self):
        self.delete_containers()
        self.delete_images()
        self.delete_files()
        self.docker_containers = []
        self.docker_images = []
        self.config_files = []

    def delete_containers(self):
        for container_id in self.docker_containers:
            self.docker_client.kill(container_id)
            self.docker_client.remove_container(container_id)

    def delete_images(self):
        for image_id in self.docker_images:
            self.docker_client.remove_image(image_id)


    def delete_files(self):
        for _file in self.config_files:
            os.remove(_file)

    #waits for Ctr+C from user and cleans up the container (used in manual app run)
    def signal_handler(self, signal, frame):
        self.clean_environment()
        try:
            print("\nApp-specific container has been stopped.")
            sys.exit(0)
        except:
            pass

    def print_engine_exception(self):
        print("ExecutionEngine EXCEPTION:\n")
        traceback.print_exc()
        print("\n")
