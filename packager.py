#!/usr/bin/env python

import os
import settings
import zipfile
from optparse import OptionParser
import shutil

class Packager():
    def __init__(self):
        pass

# Packs the application and config to a zip file
    def pack(self, app_name, container_name):
        app_path =  settings.applications_path + app_name
        zip_name = app_name + "__" + container_name
        config_path = settings.configurations_path + zip_name
        if (not(os.path.exists(app_path))):
            raise OSError("Application does not exist: " + app_name)
        self.ziptree(zip_name, "app" , app_path, "w")
        self.ziptree(zip_name, "config", config_path, "a")
        print ("Package " + "'" + app_name + container_name + ".zip' is created in '" + settings.current_path + "' folder.")  

#helper method for zip packing
    def ziptree(self, root, ziproot, tree, mode):
        try:
            zipf = zipfile.ZipFile(root + ".zip", mode, zipfile.ZIP_DEFLATED)
            for dirname, _, files in os.walk(tree):
                for filename in files:
                    absname = os.path.abspath(os.path.join(dirname, filename))
                    arcname = absname[len(os.path.abspath(tree)):]          
                    zipf.write(absname, "./" + ziproot + "/" + arcname)
        except Exception as error:
            print("Packager error %s" % error)
        finally:
            zipf.close()

# Unpacks application and config from a zip file
    def unpack(self, package_path, new_app_name):
        package_name = os.path.basename(package_path)
        if (os.path.isfile(package_name) and package_name.endswith(".zip")):
            app_name = package_name.split("__")[0] if new_app_name == None else new_app_name
            config_name = package_name.replace(".zip","") if new_app_name == None else new_app_name + "__" + package_name.replace(".zip","").split("__")[1]
         
            new_app_dir = settings.applications_path + app_name
            new_config_dir = settings.configurations_path + config_name
            self.unziptree("app/", new_app_dir, package_path)
            self.unziptree("config/", new_config_dir, package_path)         
        else:
            raise OSError("\"" + package_name + "\" is not a zip file or such file does not exist.")

    def unziptree(self, source_folder, dest_folder, zip_file):
        try:
            temp_folder = "./temp"
            os.mkdir(temp_folder)
            zipf = zipfile.ZipFile(zip_file, "r")
            for name in zipf.namelist():
                if (name.startswith(source_folder)):
                    zipf.extract(name, temp_folder)
            shutil.copytree(temp_folder+"/"+source_folder, dest_folder)
            shutil.rmtree(temp_folder)               
        except Exception as error:
            raise OSError(error)

#TODO: add help output
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--pack", action="store", dest="app_name_pack", help="Application name", metavar="APP_NAME")
    parser.add_option("--container", action="store", dest="container_name", help="Application-specific container name", metavar="CONTAINER_NAME")
    parser.add_option("--unpack", action="store", dest="package_path", help="Unpack to the location", metavar="LOCATION")
    parser.add_option("--installName", action="store", dest="app_name_install", help="Specify a new name for the application that is being installed", 
                      metavar="NEW_APP_NAME")

    (options, args) = parser.parse_args()
   
    if (options.app_name_pack and options.container_name):
        Packager().pack(options.app_name_pack, options.container_name)
    elif (options.package_path):
        Packager().unpack(options.package_path, options.app_name_install)
    else:
        print("Bad arguments... (TODO)")

