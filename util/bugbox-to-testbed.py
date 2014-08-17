#!/usr/bin/env python

import os
import shutil
import sys

sys.path.append(os.path.dirname(".."))
import settings

IGNORE_PATTERNS = ('.DS_Store')

def copy_application(src, dst):

    application_name = os.path.basename(src)

    if not os.path.exists(dst):
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns(IGNORE_PATTERNS))
        os.remove(dst+"/__init__.py")
        os.remove(dst+"/__init__.pyc")
        
        app_files = os.listdir(dst+"/application/")
        app_files = [dst+"/application/"+filename for filename in app_files]
        
        for file in app_files:
            shutil.move(file, dst)
    
        os.rmdir(dst+"/application/")

        #every wordpress plugin becomes a new application
        if (dst.find("wordpress") != -1 and os.path.exists(dst+"/plugins/")):
            plugins = os.listdir(dst+"/plugins/")

            if(".DS_Store" in plugins):
                plugins.remove(".DS_Store")

            plugins = [dst+"/plugins/"+filename for filename in plugins]
            
            for plugin in plugins:
                
                plugin_name = os.path.basename(plugin)
                plugin_dst = settings.applications_path+application_name+"_"+plugin_name
                
                shutil.copytree(dst,plugin_dst, ignore=shutil.ignore_patterns(IGNORE_PATTERNS))
                
                os.makedirs(plugin_dst+"/wp-content/plugins/"+plugin_name.split("_")[0]+"/")

                if(os.path.isfile(plugin_dst+"/plugins/"+plugin_name+"/database.sql")):
                    shutil.move(plugin_dst+"/plugins/"+plugin_name+"/database.sql", plugin_dst+"/wp-content/plugins/"+plugin_name.split("_")[0]+"/")
                
                plugin_files = os.listdir(plugin_dst+"/plugins/"+plugin_name+"/plugin/")
                plugin_files = [plugin_dst+"/plugins/"+plugin_name+"/plugin/"+filename for filename in plugin_files]
                
                for plugin_file in plugin_files:
                    shutil.move(plugin_file, plugin_dst+"/wp-content/plugins/"+plugin_name.split("_")[0]+"/")

                shutil.rmtree(plugin_dst+"/plugins/")
                generate_configuration(application_name+"_"+plugin_name, plugin_name=plugin_name)

    else:
        print("application " +dst+ " already imported")

def generate_configuration(application_name, plugin_name=""):
    dest_folder = settings.configurations_path+"/"+application_name+"__ubuntu-apache-mysql"

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
        
        db_user="dbroot"
        db_password="connection452"

        #rewrite the host in the wordpress database
        if "wordpress" in application_name:
            
            database_path = settings.applications_path+application_name
            
            database = open(database_path+"/database.sql",'r')
            database_temp = open(database_path+"/database.sql.temp",'w')

            for line in database.readlines():
                new_line = line.replace("127.0.0.1", "localhost:"+str(settings.mapped_port_out))
                database_temp.write(new_line)
    
            database.close()
            database_temp.close()
            os.remove(database_path+"/database.sql")
            os.rename(database_path+"/database.sql.temp", database_path+"/database.sql")
                
    
        dockerfile = open(dest_folder+"/Dockerfile",'w')
        dockerfile_data = generate_dockerfile(application_name)
        dockerfile.write(dockerfile_data)
        dockerfile.close()

        runfile = open(dest_folder+"/run.sh",'w')
        runfile_data = generate_runfile(db_user, db_password, plugin_name=plugin_name)
        runfile.write(runfile_data)
        runfile.close()
    
    else:
        print("configuration " +dest_folder+ " already exists")

def generate_dockerfile(application_name):
    
    application_name = application_name.split("_")[0]
    
    data ="""
FROM testbed/ubuntu-apache-mysql
MAINTAINER danielrs

RUN mkdir /var/www/%s/

ADD . /var/www/%s/

RUN chown -R www-data.www-data /var/www/%s/

RUN chmod +x /var/www/%s/run.sh
CMD cd /var/www/%s && ./run.sh
""" % (application_name,application_name,application_name,application_name, application_name)
    return data

def generate_runfile(db_user, db_password, plugin_name=""):
    data ="""
#!/bin/bash
mysqld_safe &
sleep 5

mysql < database.sql

"""

    if (plugin_name != ""):
        data+="""mysql < wp_content/plugins/%s/database.sql""" % (plugin_name)


    data+="""

echo "GRANT ALL PRIVILEGES ON *.* TO '%s'@'localhost' IDENTIFIED BY '%s' WITH GRANT OPTION" | mysql

apache2ctl start

#the container must keep running :)
while :;
do
:;
done
""" % (db_user, db_password)

    return data

if __name__ == "__main__":
    src = sys.argv[1]

    if(src == "--all"):
        
        bugbox_path = "/Users/danielrs/Dropbox/research/work/code/js-testbed/BugBox/framework/Targets/"
        applications = os.listdir(bugbox_path)
        applications = [bugbox_path+filename for filename in applications]
    
        for application in applications:
            if os.path.isdir(application):
                application_name = os.path.basename(application)
                dst = settings.applications_path + application_name
                copy_application(application,dst)
                generate_configuration(application_name)

    else:
        application_name = os.path.basename(src)
        dst = settings.applications_path + application_name
        copy_application(src,dst)
        generate_configuration(application_name)


