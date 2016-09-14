########################################################################################################################
#                                                                                                                      #
# NetApp -Jenkins Plugin using Docker container                                                                        #
# Copyright 2016 NetApp, Inc.                                                                                          #
#                                                                                                                      #
# The python scripts in this folder and others, allow CI admin and the developer a plugin that integrates              #
# with Cloudbees Jenkins Enterprise using NetApp ONTAP APIs to provide an automated continuous Integration (CI)        #
# pipeline using Gitlab, Docker container and persistent storage using NetApp Docker Volume Plugin (nDVP) for ONTAP.   #
#                                                                                                                      #
# Maintained By:  Shrivatsa Upadhye (shrivatsa.upadhye@netapp.com)                                                     #
#                 Akshay Patil (Akshay.Patil@netapp.com)                                                               #
#                                                                                                                      #
########################################################################################################################

import argparse
import subprocess
from subprocess import call

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Passing variables to the program')
    parser.add_argument('-ptz','--pathtozip', help='Path to zip inside the workspace',dest='pathtozip',required=True)
    parser.add_argument('-zip','--zipfile', help='Name of the zipfile',dest='zfile',required=True)

    globals().update(vars(parser.parse_args()))

    print "Unzipping the File..."
    tempDirName = "temp"
    tempdir_cmd = "mkdir {}/{}".format(pathtozip,tempDirName)
    return_code = subprocess.call(tempdir_cmd,shell=True)

    templocation = pathtozip + tempDirName 
    unzip_cmd = "unzip {}{} -d {}/".format(pathtozip,zfile,templocation)
    return_code = subprocess.call(unzip_cmd,shell=True)
    copywar_cmd = "cp /tmp/vol2/war/target/jenkins.war {}/wars/jenkins.war/".format(templocation)
    return_code = subprocess.call(copywar_cmd,shell=True)
   
    zip_cmd = "zip -r {}{} *".format(pathtozip,zfile,tempDirName)
    return_code = subprocess.call(zip_cmd,shell=True,cwd=templocation)
    
    deleteTempDir_cmd = "rm -rf {}".format(templocation)
    return_code = subprocess.call(deleteTempDir_cmd,shell=True)

    gitemail = "test@netapp.com"
    gituser = "Gituser"
    gitconfig_cmd = "git config --global user.email {}".format(gitemail)
    return_code = subprocess.call(gitconfig_cmd,shell=True)
    
    gitconfiguser_cmd = "git config --global user.name {}".format(gituser)
    return_code = subprocess.call(gitconfiguser_cmd,shell=True)

    gitadd_cmd = "git add -A"
    return_code = subprocess.call(gitadd_cmd,shell=True)

    gitcommit_cmd = "git commit -m 'Pushed Updated Deployment Zip'"
    return_code = subprocess.call(gitcommit_cmd,shell=True)

    print "Target War File copied... Uploading the file to Repository !!"

